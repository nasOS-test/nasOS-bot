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
from threading import Thread
from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix = settings['prefix'])
menu = DefaultMenu(page_left="⏮️", page_right="⏭️", remove="❌", active_time=60)
bot.help_command = PrettyHelp(menu=menu)
from database import rankup, getrank, mkwarn, getwarns, getServerSettings, setServerSettings

###Web

def WebServer():
    app = Flask(__name__)
    app.secret_key = bytes(os.environ["SECRET"], "UTF-8")
    app.config["DISCORD_CLIENT_ID"] = settings["id"]   # Discord client ID.
    app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
    app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
    app.config["DISCORD_BOT_TOKEN"] = settings["token"]
    discord2 = DiscordOAuth2Session(app)
    @app.route("/login/")
    def login():
        return discord2.create_session()
    @app.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        return redirect(url_for("login"))
    @app.route("/")
    @requires_authorization
    def me():
        user = discord.fetch_user()
        return render_template("user.html", user=user, rank=getrank(user.id))
    @app.route("/callback/")
    def callback():
        discord.callback()
        return redirect("/")
    app.run(int(os.environ["PORT"]))


thr = threading.Thread(target=WebServer)
thr.start()

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
    if ctx.message.author.id == ctx.guild.owner.id:
        ss = getServerSettings(ctx.guild.id)
        ss["adminRoleID"] = str(id)
        setServerSettings(ss)
        await ctx.reply("OK")
    else: await ctx.reply("Only server owner can do this")
@bot.command()
async def warns(ctx, userid):
    w = getwarns(str(userid))
    for warn in w:
        await ctx.reply(warn)
@bot.command()
async def rank(ctx):
  rank = "**"+str(getrank(ctx.message.author.id))+"** \n\n This rank is common on all servers"
  await ctx.reply(rank)
#@bot.command()
#async def number(ctx):
#    lst = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
#    ans = __import__("random").choice(lst)
#    msg = await ctx.reply("Guess the number from 0 to 9")
#    for a in lst:
#        msg.add_reaction(a)
#    while True:
#        for r in msg.reactions:
#            users = await r.users().flatten()
#            if ctx.message.author in users:
#                if r.emoji == ans:
#                    await ctx.reply("Right! The number was "+ans)
#                else:
#                    await ctx.reply("Incorrect, the number was "+ans)
#.               break
#    __import__("time").sleep(1)
@bot.command(help="Say hello")
async def hello(ctx): 
    author = ctx.message.author
    print("Hello, %s" % author)
    await ctx.reply("Hello, %s" % author)
@bot.command(help="Send message 30 times")
async def spam(ctx, st):
    author = ctx.message.author
    print(author)
    for x in range(0, 30):
        print("%s" % st)
        await ctx.reply("%s" % st)
@bot.command(help="Write text") 
async def write(ctx, arg): 
    t = str(arg)
    author = ctx.message.author
    print(author, t)
    await ctx.reply(t)
@bot.command()
async def friend(ctx): await ctx.message.author.reply_friend_request()
@bot.command()
async def warn(ctx, arg, txt):
    tt = str(arg)
    txt = str(txt)
    author = ctx.message.author.id
    adm = getServerSettings(ctx.guild.id)["adminRoleID"]
    if adm and ctx.guild.get_role(adm) in ctx.message.author.roles:
        await ctx.reply(mkwarn(userid=tt, serverid=str(ctx.guild.id), roleid=adm, txt=txt))
    else:
        await ctx.reply(mkwarn(userid=0, serverid=str(ctx.guild.id), roleid=0, txt=txt))
@bot.command()
async def date(ctx):
    author = ctx.message.author
    await ctx.reply("Дата:" + str(datetime.date.today()))
    print("Дата:" + str(datetime.date.today()) + author)
@bot.command()
async def invite(ctx):
    author = ctx.message.author
    print("This bot can be invited through a link: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot", author)
    await ctx.reply("This bot can be invited through a link: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot")
@bot.command()
async def nasOS(ctx):
    author = ctx.message.author
    print(author)
    await ctx.reply("Our site: \n http://nas-os.ml/")
@bot.command(help="Send a meme")
async def meme(ctx):
    response = requests.get('https://some-random-api.ml/meme') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Meme') # Создание Embed'a
    embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a
    await ctx.reply(embed = embed) # Отправляем Embed
@bot.command()
async def about_fox(ctx):
    response = requests.get('https://some-random-api.ml/facts/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON
    await ctx.reply(json_data['fact']) # Отправляем Embed
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f'User {member} has kicked.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f'User {member} has banned.')
    
@bot.command()
async def unban(ctx, member: discord.Member):
    await member.unban(reason=reason)
    await ctx.reply(f'User {member} has unbanned.')
    
@bot.command()
async def avatar(ctx, member: discord.Member):
    await ctx.reply(member.avatar_url)
@bot.command(help="Text to speech. \nUsage: n!tts text language")
async def tts(ctx, text, lang):
 text = str(text)
 lang = str(lang)
 a = gTTS(text, lang=lang)
 print(a)
 a.save("tts.mp3")
 await ctx.reply(file=discord.File("tts.mp3"))
@bot.command()
async def demotivator(ctx, a=" ", b=" "):
 a=str(a); b=str(b)
 for attach in ctx.message.attachments:
  await attach.save("pic.png")
 d = Demotivator(a,b)
 d.create("pic.png", fonttext="CALIBRI.TTF")
 await ctx.reply(file=discord.File("demresult.jpg"))
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
   await ctx.reply(b)
@bot.command()
async def calc(ctx, t):
  t = str(t)
  t = Template("{{"+t+"}}").render(abs=abs, i=1j)
  try:
    t = int(t)
    await ctx.reply(t)
  except ValueError:
    try:
      t = complex(t)
      await ctx.reply(f"Реальная часть: {t.real}\nМнимая часть: {t.imag}")
    except ValueError:
      await ctx.reply(t)
@bot.command()
async def httpcat(ctx, err="arbeb"):
    if err == "arbeb":
        err = random.choice([100,101,102,200,201,202,203,204,205,206,207,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,420,421,422,423,424,425,426,429,431,444,450,451,498,499,500,501,502,503,504,505,506,507,508,509,510,511,521,523,525,599])
    r = requests.get("http://http.cat/"+str(err))
    f = open("tmp.jpg", "wb")
    f.write(r.content)
    f.close()
    await ctx.send(file=discord.File("tmp.jpg"))
@bot.command()
async def qr(ctx, txt):
    r = requests.get("https://quickchart.io/qr?text="+str(txt))
    f = open("tmp.png", "wb")
    f.write(r.content)
    f.close()
    await ctx.send(file=discord.File("tmp.png"))
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
