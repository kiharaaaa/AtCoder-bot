# 提出結果を通知

import datetime
from zoneinfo import ZoneInfo
import time
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

def exe():
    now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    d = datetime.datetime(now.year, now.month, now.day-1, 0, 0, 0)
    epoch_second = int(time.mktime(d.timetuple()))  # UNIX時間を取得
    maxAC = 0

    lines=[]
    colors = ['blue', 'orange', 'green', 'red']
    with open("setting.txt", "r") as f:
        lines = f.readlines()
    members = lines[4].split()
    members.pop(0)
    num = len(members)

    # X軸 (日付)
    X = []
    now_tmp = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    now_tmp -= datetime.timedelta(days=11)
    now_month = now_tmp.month
    for i in range(10):
        now_tmp += datetime.timedelta(days=1)
        if i == 0:
            x = str(now_tmp.month) + "/" + str(now_tmp.day)
        elif now_month == now_tmp.month:
            x = str(now_tmp.day)
        else:
            x = str(now_tmp.month) + "/" + str(now_tmp.day)
            now_month = now_tmp.month
        X.append(x)

    list = []
    handles = []
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
                if epoch_second <= p['epoch_second'] and p['epoch_second'] <= epoch_second + 86400:
                    accepted.append(p_id)
                    cnt += 1

        # Y軸 (AC数)
        Y = [cnt]

        # Current Streak
        streak = 1
        streakFlag = True
        if cnt == 0:
            streak = 0
            streakFlag = False
        Ysize = 10

        while True:
            ACflag = False
            epoch_second -= 86400
            url = f'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user=' + members[i] + '&from_second=' + str(epoch_second)
            response = requests.get(url).json()
            ACcnt = 0
            for p in response:
                if epoch_second <= p['epoch_second'] and p['epoch_second'] <= epoch_second + 86400:
                    if p['result'] == 'AC':
                        ACcnt += 1
                        ACflag = True
            if ACflag and streakFlag:
                streak += 1
            else:
                streakFlag = False

            if Ysize > 1:
                Y.append(ACcnt)
                Ysize -= 1
            else:
                if ACflag == False:
                    break
        Y.reverse()
        if max(Y) > maxAC:
            maxAC = max(Y)
        line, = plt.plot(X, Y, label=members[i], color=colors[i])
        handles.append(line)
        list.append([members[i], cnt, streak])
    list = sorted(list, reverse=True, key=lambda x: x[1])
    plt.xlabel('日付')
    plt.ylabel('AC数')
    plt.yticks(np.arange(0, maxAC+1, 1))
    plt.legend(handles, members, loc="upper left")
    plt.savefig('ACgraph.png')

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
