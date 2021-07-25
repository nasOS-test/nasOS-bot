# -*- coding: utf-8 -*-
import discord
import datetime
import random
from discord.ext import commands
from config-2 import settings
import time
import json
import requests
bot = commands.Bot(command_prefix = settings['prefix'])
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="nasOS is the best")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")
@bot.command()
async def hello(ctx): 
    author = ctx.message.author
    print("Привет, %s" % author)
    await ctx.send("Привет, %s" % author)
@bot.command()
async def spam(ctx, st):
    author = ctx.message.author
    print(author)
    for x in range(0, 30):
        print("%s" % st)
        await ctx.send("%s" % st)
@bot.command() 
async def write(ctx, arg): 
    t = str(arg)
    author = ctx.message.author
    print(author, t)
    await ctx.send(t)
@bot.command()
async def warn(ctx, arg):
    tt = str(arg)
    author = ctx.message.author
    print(author, "Участнику %s вынеcно предупреждение!" % tt)
    await ctx.send("Участнику %s вынеcно предупреждение!" % tt) #отправляем обратно аргумент
@bot.command()
async def date(ctx):
    author = ctx.message.author
    await ctx.send("Дата:" + str(datetime.date.today()))
    print("Дата:" + str(datetime.date.today()) + author)
@bot.command()
async def invite(ctx):
    author = ctx.message.author
    print("Бота можно добавить по ссылке: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot", author)
    await ctx.send("Бота можно добавить по ссылке: \n" + "https://discord.com/api/oauth2/authorize?client_id=806926827552899094&permissions=8&scope=bot")
@bot.command()
async def nasOS(ctx):
    author = ctx.message.author
    print(author)
    await ctx.send("Наш сайт: \n http://nas-os.ml/")
@bot.command()
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
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
