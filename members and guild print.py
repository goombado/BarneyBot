import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'nuh uh'
GUILD = '210716706501296128'

client = discord.Client()

@client.event
async def on_ready():
#    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    for guild in client.guilds:
        if str(guild.id) == GUILD:
            break
        #if guild.name == GUILD:
        #    break
    print(
        f'{client.user} has connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

client.run(TOKEN)