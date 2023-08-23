# 提出結果を通知

import datetime
import time
import requests
from bs4 import BeautifulSoup

def exe():
    now = datetime.datetime.now()
    now -= datetime.timedelta(hours=9)
    d = datetime.datetime(now.year, now.month, now.day-1, 0, 0, 0)
    epoch_second = int(time.mktime(d.timetuple()))  # UNIX時間を取得

    lines=[]
    with open("setting.txt", "r") as f:
        lines = f.readlines()
    members = lines[3].split()
    members.pop(0)
    num = len(members)

    list = []
    epoch = epoch_second
    for i in range(num):
        epoch_second = epoch
        # 本日のAC数
        url = f'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=' + members[i] + '&from_second=' + str(epoch_second)
        response = requests.get(url).json()
        accepted = []
        cnt = 0
        for p in response:
            p_id = p['problem_id']

            if p['result'] != 'AC':
                continue
            if p_id not in accepted:
                accepted.append(p_id)
                cnt += 1

        # Current Streak
        streak = 0
        if cnt != 0:
            while True:
                streak += 1
                flag = True
                epoch_second -= 86400
                url = f'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=' + members[i] + '&from_second=' + str(epoch_second)
                response = requests.get(url).json()
                for p in response:
                    if epoch_second <= p['epoch_second'] and p['epoch_second'] <= epoch_second + 86000:
                        if p['result'] == 'AC':
                            flag = False
                            break
                if flag:
                    break
        list.append([members[i], cnt, streak])
    list = sorted(list, reverse=True, key=lambda x: x[1])
    print(list)

    text = ""
    for i in range(num):
        n = len(list[i][0])
        text += "```"
        text += list[i][0] + " " * (10-n) + ": " + str(list[i][1]) + "問"
        if list[i][2] != 0:
            text += " (" + str(list[i][2]) + "日連続)"
        text += "```"
        if i != num - 1:
            text += "\n"
    return text

exe()
