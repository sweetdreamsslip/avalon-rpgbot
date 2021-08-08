from decouple import config
import discord
from discord.ext import commands
import pymongo
import random


client = pymongo.MongoClient(config("MONGO_CONNECTION"))
db = client['avalon']
characters = db['characters']


import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


BOT_TOKEN = config('BOT_TOKEN')
PREFIX = "a!"
SPEC4 = 842178792821620768


description = 'Pronto pra matar dinheiro e ganhar dragão!'
activity = discord.CustomActivity(name="Ainda em construção! :warning:")

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix=PREFIX, description=description, activity=activity)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    await bot.change_presence(
      status = discord.Status.online,
      activity = discord.Activity(type=discord.ActivityType.listening, name="Em construção :warning:")
    )

@bot.command()
async def bomdia(ctx):
    print(dir(ctx.author))
    await ctx.channel.send("Bom dia <@{}>!".format(ctx.author.id))
    await ctx.channel.send("{}".format(ctx.author.id))
    await ctx.channel.send("{}".format(ctx.author.avatar_url))

@bot.command()
async def anon(ctx, user: discord.Member, message: str):
    await user.send(message)

@bot.command()
async def ignis(ctx):
    ignis = characters.find_one({"owner_id": "91347277993476096"})
    print(ignis)
    await ctx.channel.send(
        "Name: {}\nLevel: {}\nEXP: {}\nGold: {}".format(ignis['name'], ignis['level_total'], ignis['exp'], ignis['gold'])
    )

@bot.command()
async def set_char(ctx, exp: int):
    ignis = characters.find_one()
    characters.update_one(
        {"owner_id": str(ctx.author.id)},
        {"$set": {"exp": exp}}
    )
    await ctx.send("Job's done!")


@bot.command()
async def ajuda(ctx):
    try:
        await ctx.author.send("Ainda estou em construção :fist::pensive:")
    except discord.errors.Forbidden:
        await ctx.channel.send("Seu privado é bloqueado, não consigo te mandar mensagem")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "bebida" in message.content.lower():
        await message.channel.send("Senta aí, qual bebida você quer?")
    print("{}: {}: {}".format(message.channel, message.author, message.content))
    await bot.process_commands(message)

bot.run(BOT_TOKEN)
