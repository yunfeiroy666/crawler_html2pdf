# -*- encoding=utf-8 -*-

import time
from http import cookiejar
import requests
from bs4 import BeautifulSoup

headers = {"Host": "www.zhihu.com", "Referer": "https://www.zhihu.com/",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

# login cookie
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")
try:
    print(session.cookies)
    session.cookies.load(ignore_discard=True)
except:
    print("no cookie")


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf


# get yanzhengma
def get_captcha():
    '''
    把验证码保存到当前目录，手动识别验证码
    :return:
    '''
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码:")
    return captcha


def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_captcha(),
        "captcha": get_captcha(),
        "remember_me": 'true'
    }
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])
    for i in session.cookies:
        print(i)
    session.cookies.save()


if __name__ == "__main__":
    email = "email_address"
    password = "password"
    login(email, password)
