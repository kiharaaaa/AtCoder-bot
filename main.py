import discord
from discord.ext import tasks
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import os

from keep_alive import keep_alive
import func_schedule
import func_submissions
import func_rate_update

# 本文 ---------------------------------------------------
f = open('setting.txt', 'r')  # トークン、チャンネルIDを読み込む
datalist = f.readlines()
TOKEN = datalist[0][7:]
CHANNEL_ID_schedule = int(datalist[1][21:])
CHANNEL_ID_submissions = int(datalist[2][24:])
CHANNEL_ID_rate_update = int(datalist[3][24:])
f.close()
client = discord.Client(intents=discord.Intents.all())
keep_alive()
nextContest = ""
rateFlag = False
# -------------------------------------------------------


# 定数定義 -----------------------------------------------
ABC = 'AtCoder Beginner Contest'
ARC = 'AtCoder Regular Contest'
AGC = 'AtCoder Grand Contest'
# -------------------------------------------------------


# 開始時 -------------------------------------------------
@client.event
async def on_ready():
  minute.start()
# -------------------------------------------------------


# メッセージ受信時（デバッグ用）------------------------------
@client.event
async def on_message(message):
  # 受信したメッセージの送信者が自分の時
  if message.author.bot:
    return
# -------------------------------------------------------


# 1分に1回起動する関数 -------------------------------------
#  ・前日のリマインド
#  ・1時間前のリマインド
#  ・10分前のリマインド
#  ・その日のAC数を通知する機能
@tasks.loop(seconds=60)
async def minute():
  dayOfWeek = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%A')
  time      = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%H:%M')

  if dayOfWeek == 'Friday' and time == '09:00':  # 毎週金曜9:00に今週のコンテスト予定を通知
    await remind_yesterday()

  elif time == '20:00':  # コンテストの1時間前にリマインド
    await remind_today(60)

  elif time == '20:50':  # コンテストの10分前にリマインド
    await remind_today(10)

  elif time == '00:05':  # 毎日0:05にAC数を通知
    await notification_AC()

  if rateFlag:
    await notification_rate()
# -------------------------------------------------------


# 今週のコンテスト予定を通知 ---------------------------------
async def remind_yesterday():
  contents = func_schedule.exe()
  channel = client.get_channel(CHANNEL_ID_schedule)
  embed = discord.Embed(title="今週のコンテスト予定", color=0x00ff00)
  await channel.send(embed=embed)

  for content in contents:
    date = content[0]
    title = content[1]
    url = content[2]
    flag = False

    if ABC in title:
      embed = discord.Embed(title=title, color=0x0000ff, description=date, url=url)
      flag = True

    elif ARC in title:
      embed = discord.Embed(title=title, color=0xfd7e00, description=date, url=url)
      flag = True

    elif AGC in title:
      embed = discord.Embed(title=title, color=0xff0000, description=date, url=url)
      flag = True

      if flag:
        await channel.send(embed=embed)
# -------------------------------------------------------


# コンテストの直前に通知 ------------------------------------
async def remind_today(minutes):
  contents = func_schedule.exe()
  channel = client.get_channel(CHANNEL_ID_schedule)

  for content in contents:
    date = content[0]
    title = content[1]
    url = content[2]
    flag = False
    message = '@everyone\n'
    now_date = str(datetime.now())

    if date[0:10] != now_date[0:10]:
      continue

    if ABC in title:
      n = title.find(ABC)
      m = len(ABC)
      title = title[n : n + m + 4]
      nextContest = "abc" + title[m + 1 : m + 4]
      print(nextContest)
      if minutes == 60:
        message += '**' + title + '** まであと1時間です'
      elif minutes == 10:
        message += '**' + title + '** まであと10分です'
      flag = True

    elif ARC in title:
      n = title.find(ARC)
      m = len(ARC)
      title = title[n : n + m + 4]
      nextContest = "arc" + title[m + 1 : m + 4]
      if minutes == 60:
        message += '**' + title + '** まであと1時間です'
      elif minutes == 10:
        message += '**' + title + '** まであと10分です'
      flag = True

    elif AGC in title:
      n = title.find(AGC)
      m = len(AGC)
      title = title[n : n + m + 4]
      nextContest = "agc" + title[m + 1 : m + 4]
      if minutes == 60:
        message += '**' + title + '** まであと1時間です'
      elif minutes == 10:
        message += '**' + title + '** まであと10分です'
      flag = True

    if flag:
      rateFlag = True
      await channel.send(message)
# -------------------------------------------------------


# AC数を通知 ---------------------------------------------
async def notification_AC():
  contents = func_submissions.exe()
  channel = client.get_channel(CHANNEL_ID_submissions)

  n = datetime.now(ZoneInfo("Asia/Tokyo"))
  embed = discord.Embed(title=str(n.month) + "/" + str(int(n.day) - 1) +" AC数", description=contents, color=0x00ff00)
  await channel.send(embed=embed)
  await channel.send(file=discord.File('ACgraph.png'))
# -------------------------------------------------------


# レート更新を通知 -----------------------------------------
async def notification_rate():
  channel = client.get_channel(CHANNEL_ID_rate_update)
  flag, list = func_rate_update(nextContest)

  if flag:
    if nextContest[:3] == "abc":
      title = ABC + " " + nextContest[3:]
      color = 0x00ff00
    elif nextContest[:3] == "arc":
      title = ARC + " " + nextContest[3:]
      color = 0xfd7e00
    elif nextContest[:3] == "agc":
      title = AGC + " " + nextContest[3:]
      color = 0xff0000

    contents = ""
    for l in list:
      contents += "```" + l[0] + " " * (10 - len(l[0])) + ": "
      contents += " " * (4 - len(l[1])) + l[1] + " -> "
      contents += " " * (4 - len(l[2])) + l[2]
      contents += " (" + " " * (3 - len(l[3])) + l[3] + ")\n"
      contents += "             performance : " + " " * (4 - len(l[4])) + l[4] + ""
      contents += "```"
    embed = discord.Embed(title=title, description=contents, color=color)
    await channel.send(embed=embed)
    rateFlag = False
# -------------------------------------------------------

# botを実行 ----------------------------------------------
# try:
#   client.run(TOKEN)
# except:
#   os.system("kill 1")
client.run(TOKEN)
# -------------------------------------------------------
