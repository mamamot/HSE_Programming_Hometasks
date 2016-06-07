import pymysql
import os
from datetime import datetime

# Cкрипт создает базу данных и три таблицы: пользователи, пол пользователя и посты. В теблице пользователей мы храним
# идентификатор пользователя, его возраст (0, если не указано), пол (0, 1, 2 для значений не указано, женский и
# мужской). В таблице пол хранятся строковые репрезентации для пола. В таблице постов хранятся идентификатор
# пользователя, дата создания поста и текст поста (TEXT).

HOST = "localhost"
USERNAME = ""
PASSWORD = ""
DBNAME = "vk_data"


def create_db(dbname):
    connection = pymysql.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "CREATE DATABASE {}".format(dbname)
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


def create_user_table(dbname):
    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 db=dbname,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = """
                CREATE TABLE `users` (
                    `uid` int(12) NOT NULL,
                    `age` TINYINT UNSIGNED,
                    `sex` TINYINT UNSIGNED,
                    `languages` VARCHAR(255),
                    PRIMARY KEY (`uid`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

                CREATE TABLE `sex` (
                    `id` TINYINT NOT NULL,
                    `repr` VARCHAR(2) NOT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

                INSERT INTO `sex` (`id`, `repr`)
                VALUES (0, "na"), (1, "f"), (2, "m");
                """
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        print("Users and sex tables created.")
    except Exception as e:
        print(e)
    finally:
        connection.close()


def create_posts_table(dbname):
    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 db=dbname,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = """
            CREATE TABLE `posts` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `uid` int(12) NOT NULL,
                `time_created` DATETIME NOT NULL,
                `post` TEXT,
                PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            AUTO_INCREMENT=1
            """
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        print("Posts table created.")
    except Exception as e:
        print(e)
    finally:
        connection.close()


def import_users(path_to_csv, dbname):
    with open(path_to_csv, encoding="utf-8") as f:
        counter = 0
        data = list()
        for line in f:
            line = line.strip()
            if counter > 0:
                line = [x for x in line.split(",", 3)]
                if line[2] == "":
                    line[2] = 0
                line[3] = line[3].strip('"')
                line = "({},{},{},'{}')".format(*line)
                data.append(line)
            counter += 1

    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 db=dbname,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`uid`, `age`, `sex`, `languages`) VALUES {}".format(",".join(data))
            cursor.execute(sql)
        connection.commit()
        print("Users import done. {} rows created.".format(counter))
    except Exception as e:
        print(e)
    finally:
        connection.close()


def import_posts(path_to_posts, dbname):
    data = list()
    counter = 0
    for file in os.listdir(path_to_posts):
        if file.endswith(".txt"):
            with open(os.path.join(path_to_posts, file), encoding="utf-8") as f:
                uid = file.split(".")[0]
                posts = f.read().strip("\n").split(">>")[1:]
                for post in posts:
                    timestamp, text = post.split("\n", 1)
                    time_created = datetime.fromtimestamp(int(timestamp)).isoformat()
                    text = pymysql.escape_string(text.strip())
                    data.append("({},'{}','{}')".format(uid, time_created, text))
                    counter += 1

    connection = pymysql.connect(host=HOST,
                                 user=USERNAME,
                                 password=PASSWORD,
                                 db=dbname,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `posts` (`uid`, `time_created`, `post`) VALUES {}".format(",".join(data))
            cursor.execute(sql)
        connection.commit()
        print("Posts import done. {} rows created.".format(counter))
    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == "__main__":
    print("When high-performance computing meets Unecha.")
    create_db(DBNAME)
    create_posts_table(DBNAME)
    create_user_table(DBNAME)
    import_users("users.csv", DBNAME)
    import_posts("../VKDumper/posts/", DBNAME)
    print("Done.")