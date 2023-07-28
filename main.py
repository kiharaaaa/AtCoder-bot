import discord
from discord.ext import tasks
import asyncio
from datetime import datetime

import func_schedule

# 本文 ---------------------------------------------------
f = open('setting.txt', 'r')  # トークン、チャンネルIDを読み込む
datalist = f.readlines()
TOKEN = datalist[0][7:]
CHANNEL_ID_schedule = int(datalist[1][21:])
f.close()
client = discord.Client(intents=discord.Intents.all())
# -------------------------------------------------------


# 開始時 -------------------------------------------------
@client.event
async def on_ready():
    print(f'ログイン：{client.user.name}')
    schedule.start()  # 月曜9時にリマインドする機能
# -------------------------------------------------------


# メッセージ受信時（デバッグ用）------------------------------
@client.event
async def on_message(message):  
    # 受信したメッセージの送信者が自分の時
    if message.author.bot:
        return
# -------------------------------------------------------


# 月曜9時にコンテストをリマインドする機能 ----------------------
@tasks.loop(seconds=60)
async def schedule():
    now = datetime.now().strftime('%A:%H:%M')
    
    if now == 'Monday:09:00':  # 毎週月曜9:00に今週のコンテスト予定を通知
        contents = func_schedule.exe()
        channel = client.get_channel(CHANNEL_ID_schedule)
        
        embed = discord.Embed(title="今週のコンテスト予定", color=0x00ff00)
        await channel.send(embed=embed)
        
        for content in contents:
            date = content[0]
            title = content[1]
            flag = False
            
            if 'AtCoder Beginner Contest' in title:
                embed = discord.Embed(title=title, color=0x0000ff, description=date)
                flag = True
            elif 'AtCoder Regular Contest' in title:
                embed = discord.Embed(title=title, color=0xfd7e00, description=date)
                flag = True
            elif 'AtCoder Grand Contest' in title:
                embed = discord.Embed(title=title, color=0xff0000, description=date)
                flag = True
            
            if flag:
                await channel.send(embed=embed)
# -------------------------------------------------------


# botを実行 ----------------------------------------------
client.run(TOKEN)
# -------------------------------------------------------