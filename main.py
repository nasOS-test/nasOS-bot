# -*- coding: utf-8 -*-
import discord
import datetime
import random
from discord.ext import commands
from config import settings
import time
import json
from gtts import gTTS
from simpledemotivators import Demotivator
import requests
from pretty_help import DefaultMenu, PrettyHelp
bot = commands.Bot(command_prefix = settings['prefix'])
menu = DefaultMenu(page_left="⏮️", page_right="⏭️", remove="❌", active_time=60)
bot.help_command = PrettyHelp(menu=menu)
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="nasOS is the best")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")
@bot.command(help="Say hello")
async def hello(ctx): 
    author = ctx.message.author
    print("Hello, %s" % author)
    await ctx.send("Hello, %s" % author)
@bot.command(help="Send message 30 times")
async def spam(ctx, st):
    author = ctx.message.author
    print(author)
    for x in range(0, 30):
        print("%s" % st)
        await ctx.send("%s" % st)
@bot.command(help="Write text") 
async def write(ctx, arg): 
    t = str(arg)
    author = ctx.message.author
    print(author, t)
    await ctx.send(t)
@bot.command()
async def warn(ctx, arg):
    tt = str(arg)
    author = ctx.message.author
    print(author, "User %s has been warned!" % tt)
    await ctx.send("User %s has been warned!" % tt) #отправляем обратно аргумент
@bot.command()
async def date(ctx):
    author = ctx.message.author
    await ctx.send("Дата:" + str(datetime.date.today()))
    print("Дата:" + str(datetime.date.today()) + author)
@bot.command()
async def invite(ctx):
    author = ctx.message.author
    print("This bot can be invited through a link: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot", author)
    await ctx.send("This bot can be invited through a link: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot")
@bot.command()
async def nasOS(ctx):
    author = ctx.message.author
    print(author)
    await ctx.send("Our site: \n http://nas-os.ml/")
@bot.command(help="Send a meme")
async def meme(ctx):
    response = requests.get('https://some-random-api.ml/meme') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Meme') # Создание Embed'a
    embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
@bot.command()
async def about_fox(ctx):
    response = requests.get('https://some-random-api.ml/facts/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON
    await ctx.send(json_data['fact']) # Отправляем Embed
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has banned.')
    
@bot.command()
async def unban(ctx, member: discord.Member):
    await member.unban(reason=reason)
    await ctx.send(f'User {member} has unbanned.')
    
@bot.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(member.avatar_url)
@bot.command(help="Text to speech. \nUsage: n!tts text language")
async def tts(ctx, text, lang):
 text = str(text)
 lang = str(lang)
 a = gTTS(text, lang=lang)
 print(a)
 a.save("tts.mp3")
 await ctx.send(file=discord.File("tts.mp3"))
@bot.command()
async def demotivator(ctx, a=" ", b=" "):
 a=str(a); b=str(b)
 for attach in ctx.message.attachments:
  await attach.save("pic.png")
 d = Demotivator(a,b)
 d.create("pic.png", line="nasOS funny", fonttext="CALIBRI.TTF")
 await ctx.send(file=discord.File("demresult.jpg"))
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
