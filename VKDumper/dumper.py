import vk
from datetime import date
import os
from time import sleep

APPID = "5495761"
TOWNID = 716  # Унеча
# TODO: sensitive credentials here: don't commit!



def get_age(bdate):
    day, month, year = (int(x) for x in bdate.split("."))
    today = date.today()
    born = date(year, month, day)
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age


def get_and_save_users(vkapi, town, count=1000):
    users = api.users.search(city=town, count=count, fields="sex,bdate,personal")[1:]
    csv = list()
    uids = list()
    csv.append('uid,sex,age,"langs"')
    for user in users:
        uid = user['uid']
        uids.append(uid)
        sex = user['sex']
        if 'bdate' in user:
            if len(user['bdate'].split(".")) == 3:
                age = get_age(user['bdate'])
            else:
                age = ''
        else:
            age = ''
        if 'personal' in user:
            if 'langs' in user['personal']:
                langs = ",".join(user['personal']['langs'])
            else:
                langs = ''
        else:
            langs = ''
        csv.append('{},{},{},"{}"'.format(str(uid), sex, str(age), langs))
    with open("users.csv", "w", encoding="utf-8") as w:
        w.write("\n".join(csv))
    return uids


def get_and_save_posts(api, uids):
    counter = 0
    for uid in uids:
        counter += 1
        try:
            texts = list()
            posts = api.wall.get(owner_id=uid, filter="owner", count=100)[1:]
            for post in posts:
                # checking whether it is a repost or not
                if 'copy_owner_id' not in post:
                    # get rid of empty posts (photos) as well as some useless garbage like "."
                    if len(post['text']) > 2:
                        texts.append('>>{}\n{}\n'.format(post['date'], post['text']))
            if texts:
                with open(os.path.join("posts", str(uid) + ".txt"), "w", encoding="utf-8") as w:
                    w.write("\n".join(texts))
                    print("{}. Posts for {} are saved.".format(counter, uid))
        except vk.exceptions.VkAPIError as e:
            print("{}. Error reading a wall: {}".format(counter, str(e)))
        sleep(0.3)


if __name__ == "__main__":
    session = vk.AuthSession(app_id='5495761', user_login=LOGIN, user_password=PASSWORD)
    api = vk.API(session)
    # skipping the number of entries - we can only get 1000
    uids = get_and_save_users(api, TOWNID)
    sleep(0.3)
    get_and_save_posts(api, uids)
    print("Long live Unecha!")
