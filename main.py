import discord
import random
import asyncio
import numpy as np
from datetime import datetime

import func_schedule

f = open('setting.txt', 'r')
datalist = f.readlines()
TOKEN = datalist[0][7:]
CHANNEL_ID_schedule = int(datalist[1][21:])
f.close()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    now = datetime.now().strftime('%A:%H:%M')
    
    if now != 'Monday:09:00':  # 毎週月曜9:00に今週のコンテスト予定を通知
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

@client.event
async def on_message(message):  # メッセージを受信したら
    # 受信したメッセージの送信者が自分の時
    if message.author.bot:
        return 

    # 毎週月曜の9:00とかに動かしたい
    if message.content == "/schedule":
        contents = func_schedule.exe()
        channel = client.get_channel(CHANNEL_ID_schedule)
        
        embed = discord.Embed(title="今週のコンテスト", color=0x00ff00)
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

client.run(TOKEN)
