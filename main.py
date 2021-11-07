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
from jinja2 import Template
from pretty_help import DefaultMenu, PrettyHelp
import logging

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix = settings['prefix'])
menu = DefaultMenu(page_left="⏮️", page_right="⏭️", remove="❌", active_time=60)
bot.help_command = PrettyHelp(menu=menu)
from database import rankup, getrank, mkwarn, getwarns, getServerSettings, setServerSettings
class Class_a:
 def e(self, id):
  return "<:emoji:" + str(id) + ">"
 def plaintxt(self, txt):
  return txt
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="n!help")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")
@bot.event
async def on_message(message):
  await bot.process_commands(message)
  rankup(message.author.id)
@bot.command()
async def set_admin_role(ctx, id):
    if ctx.author.id == ctx.guild.owner.id:
        ss = getServerSettings(ctx.guild.id)
        ss["adminRoleID"] = str(id)
        setServerSettings(ss)
        await ctx.send("OK")
    else: await ctx.send("Only server owner can do this")
@bot.command()
async def warns(ctx, userid):
    w = getwarns(str(userid))
    for warn in w:
        await ctx.send(warn)
@bot.command()
async def rank(ctx):
  rank = "**"+str(getrank(ctx.message.author.id))+"** \n\n This rank is common on all servers"
  await ctx.send(rank)
#@bot.command()
#async def number(ctx):
#    lst = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
#    ans = __import__("random").choice(lst)
#    msg = await ctx.send("Guess the number from 0 to 9")
#    for a in lst:
#        msg.add_reaction(a)
#    while True:
#        for r in msg.reactions:
#            users = await r.users().flatten()
#            if ctx.message.author in users:
#                if r.emoji == ans:
#                    await ctx.send("Right! The number was "+ans)
#                else:
#                    await ctx.send("Incorrect, the number was "+ans)
#.               break
#    __import__("time").sleep(1)
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
async def friend(ctx): await ctx.author.send_friend_request()
@bot.command()
async def warn(ctx, arg, txt):
    tt = str(arg)
    txt = str(txt)
    author = ctx.message.author.id
    adm = getServerSettings(ctx.guild.id)["adminRoleID"]
    if adm and ctx.guild.get_role(adm) in ctx.author.roles:
        await ctx.send(mkwarn(userid=tt, serverid=str(ctx.guild.id), roleid=adm, txt=txt))
    else:
        await ctx.send(mkwarn(userid=0, serverid=str(ctx.guild.id), roleid=0, txt=txt))
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
 d.create("pic.png", fonttext="CALIBRI.TTF")
 await ctx.send(file=discord.File("demresult.jpg"))
@bot.command()
async def aboba(ctx, b="Аргумент не указан"):
   b=str(b)
   b = b.replace("a", "🅰️")
   b = b.replace("A", "🅰️")
   b = b.replace("а", "🅰️")
   b = b.replace("А", "🅰️")
   b = b.replace("b", "🅱️")
   b = b.replace("B", "🅱️")
   b = b.replace("б", "🅱️")
   b = b.replace("Б", "🅱️")
   b = b.replace("o", "🅾️")
   b = b.replace("O", "🅾️")
   b = b.replace("о", "🅾️")
   b = b.replace("О", "🅾️")
   await ctx.send(b)
@bot.command()
async def j(ctx, t):
  await ctx.send(Template(t).render(ctx=Class_a()))
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
