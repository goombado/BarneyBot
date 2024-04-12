import discord
import asyncio
import requests
import json


client = discord.Client()
token = 'what is this'

inFile = open('txt_files/chess_usernames.txt')
chess_user_dict = inFile.read()
scoreboard_id = '5ebd39d175c68e00142cba6d'


def url_get(url, headers, request, params=False):
    if request == 'POST':
        r = requests.post(url, data=json.dumps(params), headers=headers)
    elif request == 'GET':
        r = requests.get(url, headers=headers)
    return


@client.event
async def on_message(message):
    global chess_user_dict
    if message.author == client.user:
        return
    
    if message.content.lower() == 'chess':
        try:
            player_username = chess_user_dict[message.author.id]
        except:
            pass
    
    if message.content.lower() == 'embed':
        embed = discord.Embed(
            title='Test Embed',
            type='rich',
            description='This is a test description to see what embeds actually look like',
            url='https://www.google.com/',
            colour = discord.Colour(int('F48C2F', 16))
        )
        embed.set_image(url='https://www.stickpng.com/assets/images/5a5773c81c992a034569ab90.png')
        embed.set_author(name='andrei')
        embed.add_field(name='test field 1', value='this is a test field, with inline=true', inline=True)
        embed.add_field(name='test field 2', value='this is a test field, with inline=false im going to keep adding text to this to see if maybe inline affects text wrapping in some way.', inline=False)
        embed.add_field(name='test field 3', value='this is a test field, with inline=true. im going to keep adding text to this to see if maybe inline affects text wrapping in some way.', inline=True)
        embed.insert_field_at(index=1, name='test field 4', value='test field, inserted into index 1, inline=False', inline=False)
        embed.set_thumbnail(url='https://i.ytimg.com/vi/mmklUBVqdJ0/maxresdefault.jpg')
        embed.set_footer(text='this is a test footer', icon_url='https://cdn.vox-cdn.com/thumbor/qrvEsgrb8tNoho5DJWlFzkBBquY=/0x0:1440x900/1200x800/filters:focal(615x161:845x391)/cdn.vox-cdn.com/uploads/chorus_image/image/65503210/Screen_Shot_2019_10_18_at_4.30.19_PM.0.png')
        await message.channel.send(embed=embed)


client.run(token)


