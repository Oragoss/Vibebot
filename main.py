# bot.py
from config import *
import os
import random
import discord
from discord.ext import commands
import youtube_dl

TOKEN = token
GUILD = guild

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    for member in guild.members:
        # members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {member.name}')


@client.event
async def on_member_join(member):
    print(f'{member}')
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!\n Here are a list of my commands:')
    await member.dm_channel.send('TODO: INSERT COMMANDS')


# @client.event
# async def on_member_update(member):
#     print(f'{member}')
#     await member.create_dm()
#     await member.dm_channel.send(f'Hi {member.name}, I saw you update!')
#     await member.dm_channel.send('Hey hey heyo!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Cool. Cool cool cool cool cool cool cool, ',
        'no doubt no doubt no doubt no doubt.',
    ]

    if message.content == '99':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)


client.run(TOKEN)
