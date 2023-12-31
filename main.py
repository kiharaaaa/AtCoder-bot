import discord
from discord.ext import tasks
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import os

from keep_alive import keep_alive
import func_schedule
import func_submissions

# 本文 ---------------------------------------------------
f = open('setting.txt', 'r')  # トークン、チャンネルIDを読み込む
datalist = f.readlines()
TOKEN = datalist[0][7:]
CHANNEL_ID_schedule = int(datalist[1][21:])
CHANNEL_ID_submissions = int(datalist[2][24:])
f.close()
client = discord.Client(intents=discord.Intents.all())
keep_alive()

# 定数定義
ABC = 'AtCoder Beginner Contest'
ARC = 'AtCoder Regular Contest'
AGC = 'AtCoder Grand Contest'
# -------------------------------------------------------


# 開始時 -------------------------------------------------
@client.event
async def on_ready():
  schedule.start()


# -------------------------------------------------------


# メッセージ受信時（デバッグ用）------------------------------
@client.event
async def on_message(message):
  # 受信したメッセージの送信者が自分の時
  if message.author.bot:
    return


# -------------------------------------------------------


# コンテストをリマインドする機能 -----------------------------
# その日のAC数を通知する機能 --------------------------------
@tasks.loop(seconds=60)
async def schedule():
  now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%A:%H:%M')

  if now == 'Fryday:09:00':  # 毎週金曜9:00に今週のコンテスト予定を通知
    contents = func_schedule.exe()
    channel = client.get_channel(CHANNEL_ID_schedule)

    embed = discord.Embed(title="今週のコンテスト予定", color=0x00ff00)

    for content in contents:
      date = content[0]
      title = content[1]
      url = content[2]
      flag = False

      if ABC in title:
        embed = discord.Embed(title=title,
                              color=0x0000ff,
                              description=date,
                              url=url)
        flag = True
      elif ARC in title:
        embed = discord.Embed(title=title,
                              color=0xfd7e00,
                              description=date,
                              url=url)
        flag = True
      elif AGC in title:
        embed = discord.Embed(title=title,
                              color=0xff0000,
                              description=date,
                              url=url)
        flag = True

      if flag:
        await channel.send(embed=embed)

  if now[-5:] == '00:05':  # 毎日0:05にAC数を通知
    contents = func_submissions.exe()
    channel = client.get_channel(CHANNEL_ID_submissions)

    n = datetime.now(ZoneInfo("Asia/Tokyo"))
    embed = discord.Embed(title=str(n.month) + "/" + str(int(n.day) - 1) +
                          " AC数",
                          description=contents,
                          color=0x00ff00)
    await channel.send(embed=embed)
    await channel.send(file=discord.File('ACgraph.png'))
    return

  if now[-5:] == '20:00':  # コンテストの1時間前にリマインド
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
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと1時間です'
        flag = True

      elif ARC in title:
        n = title.find(ARC)
        m = len(ARC)
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと1時間です'
        flag = True

      elif AGC in title:
        n = title.find(AGC)
        m = len(AGC)
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと1時間です'
        flag = True

      if flag:
        await channel.send(message)

  if now[-5:] == '20:50':  # コンテストの10分前にリマインド
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
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと10分です'
        flag = True

      elif ARC in title:
        n = title.find(ARC)
        m = len(ARC)
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと10分です'
        flag = True

      elif AGC in title:
        n = title.find(AGC)
        m = len(AGC)
        title = title[n:n + m + 4]
        message += '**' + title + '** まであと10分です'
        flag = True

      if flag:
        await channel.send(message)


# -------------------------------------------------------

# botを実行 ----------------------------------------------
# try:
#   client.run(TOKEN)
# except:
#   os.system("kill 1")
client.run(TOKEN)
# -------------------------------------------------------
