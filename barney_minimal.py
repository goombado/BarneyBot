import time
current_time = time.time()
import datetime
import discord
import asyncio
import random
import re as regex

connected=True
token = 'rofl no token for you'
client = discord.Client()


async def period_announcer(self):
    global connected
    await self.wait_until_ready()
    guild = discord.utils.get(self.guilds, id=210716706501296128)
    channel = discord.utils.get(guild.text_channels, id=704836355070361780)
    mention = guild.default_role.mention
    green_zone_channel = discord.utils.get(guild.voice_channels, id=469410821294784512)
    bus_channel = discord.utils.get(guild.voice_channels, name="BUS")
    t4_channel = discord.utils.get(guild.voice_channels, id=691863175288586261)
    t1_channel = discord.utils.get(guild.voice_channels, id=691863169991311431)
    walk_channel = discord.utils.get(guild.voice_channels, name="WALK")
    boat_channel = discord.utils.get(guild.voice_channels, name="BOAT")
    print(f'{guild.name}, {channel.name} ')
    while connected:
        if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
            await asyncio.sleep(28800)
            continue
        else:
            if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 25 and datetime.datetime.now().second <= 2:
                await channel.send(f"It's 8:25 {mention}. 5 minutes until school starts! Woohoo!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 30 and datetime.datetime.now().second <= 2:
                await channel.send(f"It's 8:30 {mention}. Time for morning tutorial! Yay!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 40 and datetime.datetime.now().second <= 2:
                await channel.send("It's 8:40. Period 1 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 20 and datetime.datetime.now().second <= 2:
                await channel.send("It's 9:20. You have 5 minutes to get to Period 2!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 25 and datetime.datetime.now().second <= 2:
                await channel.send("It's 9:25. Period 2 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 10 and datetime.datetime.now().minute == 5 and datetime.datetime.now().second <= 2:
                await channel.send("It's 10:05. You have 5 minutes to get to Period 3!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 10 and datetime.datetime.now().minute == 10 and datetime.datetime.now().second <= 2:
                await channel.send("It's 10:10. Period 3 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 10 and datetime.datetime.now().minute == 50 and datetime.datetime.now().second <= 2:
                await channel.send("It's 10:50, recess boys.")
                for voice_channel in guild.voice_channels:
                    if voice_channel.id == 469410821294784512:
                        continue
                    for user in voice_channel.members:
                        await user.move_to(green_zone_channel)
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 7 and datetime.datetime.now().second <= 2:
                await channel.send("It's 11:07. You have 3 minutes to get to Period 4!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 10 and datetime.datetime.now().second <= 2:
                await channel.send("It's 11:10. Period 4 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 50 and datetime.datetime.now().second <= 2:
                await channel.send("It's 11:50. You have 5 minutes to get to Period 5!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 55 and datetime.datetime.now().second <= 2:
                await channel.send("It's 11:55. Period 5 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 12 and datetime.datetime.now().minute == 35 and datetime.datetime.now().second <= 2:
                await channel.send("It's 12:35, lunch time boys.")
                for voice_channel in guild.voice_channels:
                    if voice_channel.id == 469410821294784512:
                        continue
                    for user in voice_channel.members:
                        try:
                            await user.move_to(green_zone_channel)
                        except:
                            continue
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 13 and datetime.datetime.now().minute == 32 and datetime.datetime.now().second <= 2:
                await channel.send("It's 13:32. You have 3 minutes to get to Period 6!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 13 and datetime.datetime.now().minute == 35 and datetime.datetime.now().second <= 2:
                await channel.send("It's 13:35. Period 6 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 14 and datetime.datetime.now().minute == 15 and datetime.datetime.now().second <= 2:
                await channel.send("It's 14:15. You have 5 minutes to get to Period 7!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 14 and datetime.datetime.now().minute == 20 and datetime.datetime.now().second <= 2:
                await channel.send("It's 14:20. Period 7 has started!")
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 15 and datetime.datetime.now().minute == 0 and datetime.datetime.now().second <= 2:
                await channel.send(f"It's 15:00 {mention}. School's over!")
                for voice_channel in guild.voice_channels:
                    if voice_channel.id == 469410821294784512:
                        continue
                    for user in voice_channel.members:
                        try:
                            await user.move_to(green_zone_channel)
                        except:
                            continue
                await asyncio.sleep(60)
                continue
            elif datetime.datetime.now().hour == 15 and datetime.datetime.now().minute == 20 and datetime.datetime.now().second <= 2:
                await channel.send("It's 3:20. Home time!")
                for voice_channel in guild.voice_channels:
                    for user in voice_channel.members:
                        try:
                            if (user.id == 197264395196170240 or user.id == 236682223128936448 or user.id == 192957897192374272 or user.id == 240380481563131905) and (voice_channel.id != bus_channel.id): #rohan james drain jack
                                await user.move_to(bus_channel)
                            if (user.id == 203672102509740042 or user.id == 183880246917988353) and (voice_channel.id != t4_channel.id): #me steven
                                await user.move_to(t4_channel)
                            if (user.id == 185165742495367168 or user.id == 470086166503489536 or user.id == 183880560454664192 or user.id == 402764753195368448 or user.id == 188800837328306176 or user.id == 226567954551144449 or user.id == 249029217524645889 or user.id == 185285433012387840) and (voice_channel.id != t1_channel.id): #tom calvin grant schmalex maxd josh bryson ryan
                                await user.move_to(t1_channel)
                            if (user.id == 195841061531287552 or user.id == 211810742003957761) and (voice_channel.id != walk_channel.id): #ciaran max
                                await user.move_to(walk_channel)
                            if (user.id == 188483813159075840) and (voice_channel.id != boat_channel.id): #jerry
                                await user.move_to(boat_channel)
                        except:
                            continue
                await asyncio.sleep(60)
                continue
            else:
                await asyncio.sleep(2)


client.bg_task = client.loop.create_task(period_announcer(client))

@client.event
async def on_ready():
    global connected
    global current_time
    connected = False
    print(f'{client.user.name} has connected to Discord.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"))
    print(f'It took {time.time()-current_time} seconds to boot up')
    connected = True

def general_fuckery(message):
    user_dict = {
        188800837328306176: 'max',
        183880560454664192: 'retard',
        192957897192374272: 'drain',
        226567954551144449: 'josh',
        183880246917988353: 'steve',
        203672102509740042: 'andrei',
        249029217524645889: 'barney',
        240380481563131905: 'jack',
        330535151790718976: 'adam',
        236694472883175426: 'eeshwar',
        203491015808516096: 'bong',
        373033173715517440: 'dan',
        185165742495367168: 'tom',
        194323407431532544: 'eddy',
        188483813159075840: 'jezmeister',
        195841061531287552: 'schmieran',
        197264395196170240: 'rohan',
        189339029265842176: 'mort',
        470086166503489536: 'schmalvin',
        218977515404787712: 'jerome',
        186276713364324353: 'henry',
        185285433012387840: 'ryan',
        211810742003957761: 'max',
        236682223128936448: 'gnu',
        402764753195368448: 'schmalex'
    }

    barney_response_1 = [
        'hi my name barney',
        'i\'m really sad please talk to me',
        (
            'like super duper sad, '
            'i just want a friend.'
        ),
    ]

    barney_response_2 = 'you\'re really mean you know that fuck you too'
    barney_response_3 = '👋 Hello there'

    greeting_pattern = regex.compile('(^hi(?!( barney)).*)|(^hello.*)|(^hey.*)|(^howdy.*)|(^obi wan)')

    if message.content.lower() == 'barney':
        response = random.choice(barney_response_1)
        return response

    elif message.content.lower() == 'fuck you barney':
        response = barney_response_2
        return response

    elif 'hi barney' in message.content.lower():
        try:
            response = f'hi {user_dict[message.author.id]}'
        except:
            response = 'hi'
        return response

    elif greeting_pattern.search(message.content.lower()):
        response = barney_response_3
        return response

    elif 'mr 305' in message.content.lower(): # ok ciaran
        response = 'mr worldwide'
        return response

    else:
        response = None
        return response

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id != 670239186556551198: # me, i don't want general fuckery
        response = general_fuckery(message)
        if response:
            await message.channel.send(response)
        else:
            return

client.run(token)