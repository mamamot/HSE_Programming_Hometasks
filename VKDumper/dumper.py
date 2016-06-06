import vk
from datetime import date

APPID = "5495761"
TOWNID = 716  # Унеча



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
        csv.append('{},{},{},"{}"'.format(uid, sex, str(age), langs))
    with open("users.csv", "w", encoding="utf-8") as w:
        w.write("\n".join(csv))
    return uids


def get_and_save_posts(uids):
    pass


if __name__ == "__main__":
    session = vk.AuthSession(app_id='5495761', user_login=LOGIN, user_password=PASSWORD)
    api = vk.API(session)
    # skipping the number of entries - we can only get 1000
    uids = get_and_save_users(api, TOWNID)
