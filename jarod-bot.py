import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')

@client.event
async def on_message(message):
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            if ".gif" in attachment.filename.lower():
                await message.channel.send('NO GIFS')
                await message.delete()
                break
    elif len(message.embeds) > 0:
        for embed in message.embeds:
            if "gif" in embed.type.lower():
                await message.channel.send('NO GIFS')
                await message.delete()
                break

client.run("ruh roh")