# コンテストの予定を取得

import requests
from bs4 import BeautifulSoup
import datetime

def exe():
    url = 'https://atcoder.jp/contests/?lang=ja'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    elems = soup.find_all("a")

    now = str(datetime.datetime.now())[:16]
    next = str(datetime.datetime.now() + datetime.timedelta(days=7))[:16]
    flag = False
    date = ""
    schedule = []

    for elem in elems:
        try:
            s = str(elem.contents[0])
            if flag:
                schedule.append([date, s])
                flag = False
                
            if s[:5] == "<time":
                date = s[35:51]
                if now < date and date < next:
                    flag = True
                else:
                    date = ""
        except:
            continue
        
    return schedule
