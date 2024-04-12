# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODULE IMPORTS
# pip required for: discord.py[voice], asyncio, logging, requests, pytesseract, pillow, schoolopy, pyyaml
# other programs required: ffmpeg, tesseract-ocr, a valid libopus-x64.dll file (obtained from the discord.py python directory) for voice recognition
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import time
current_time = time.time()
from typing import Any, Dict, List, Tuple
import asyncio
import sys
import copy
import datetime
import io
import json
import logging
import math
import os
import random
import re as regex
import threading
from pprint import pprint
import discord
import pytesseract
import requests
import schoolopy
import yaml
from discord import FFmpegPCMAudio
from discord.ext import commands
from PIL import Image
from sympy import *
import unicodedata
import emoji
import confusables
from pyzbar import pyzbar
import numpy as np
import secrets
import qrcode
import fbchat
import subprocess
from multiprocessing import Process
import audioop
import rsa
import base64
from enum import Enum


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DISCORD.LOG LOGGER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


emoji_regex = emoji.get_emoji_regexp()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLE DECLARATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
token = 'not that easy'
GUILD = '210716706501296128'
schmalex = True
bazinga = False
mafia_game_started = False
user_voice_cooldown = {}
user_cooldown_time_remaining = {}
voice_cooldown = False
message_received = False
connected = True
steve_stream = False
previous_5_messages = []
receive_connections = 0
receive_users = []
listeners_active = {}
league_players = []
league_detection = False
token_js_dict = {
    1: ['good luck', 'baby_bop-listener.js', 'baby bop'],
    2: ['finding more', 'b_j-listener.js', 'b.j.'],
    3: ['tokens i left in places', 'riff-listener.js', 'riff']
}
whos_listening_to_who = {}
swear_pattern = regex.compile('(fuck)|(shit)') # there was more...
kpop_pattern = regex.compile(r"((k[^ ]*[pP][o0O][pP])|(k p o p)|(korean pop)|(pop(.*) korea)|(01101011 01110000 01101111 01110000)|" # BIG MATCHES
                            r"(([𐤀κk🇰ᵏ⛕片k𝕜k长k͓̽ꈵҜkқᏦｋ𝕂𝓀K<]+)|(ᖽᐸ)|(\|⊰)|(l𡿨)|(\|<)|(\|-<)|(/<)|(\:regional_indicator_k\:)|(\)<))" # K MATCHES
                            r"[.,/'\"%^&*?!@’#$()-_+=~`|<> 　]*" # SEPARATORS
                            r"(([مƤ尸ρ𐡑卩𝕡pᖘᚦρ९ⓟקp͓̽𝓅Ƥᕵየ𐡒ƤƿᕿꉣᎮ𝓟pþمр𝔭🇵РP]+)|(\|>)|(\|ˀ)|(/>)|(,o)|(\|?)|(\:parking\:)|(\:regional_indicator_p\:))" # P MATCHES 1
                            r"[.,/'\"%^&’*?!@#$()-_+=~`|<> 　]*" # SEPARATORS
                            r"(([םo𓆠Q𓍶@口🇴़𓃿鬱õºο𓇳𓄣.๏૦𓂒𓂸๐𝓸°ᵒ𓃯𐡈ꁏoᎧσ〇Ⓞᓎ回𑀩𝕠θㆁôōㄖøo͓̽оðО٥סּᓍ0O]+)|c *ɔ|(< *>)|(\{ *\})|(\[o\])|(\( *\))|(\:regional_indicator_o\:))" # O MATCHES
                            r"[.,/'\"%^&*?!@#’$()-_+=~`|<> 　]*" # SEPARATORS
                            r"(([مƤ尸ρ𐡑卩𝕡pᖘᚦ९ρקp͓̽ⓟ𝓅Ƥᕵየ𐡒Ƥƿᕿ𝓟ꉣpᎮþمр𝔭🇵РP]+)|(\|>)|(\|ˀ)|(/>)|(,o)|(\|?)|(\:parking\:)|(\:regional_indicator_p\:)))") # P MATCHES 2
user_dict = {
        188800837328306176: 'user1',
        183880560454664192: 'user2',
        192957897192374272: 'user3',
        226567954551144449: 'user4',
        183880246917988353: 'user5',
        203672102509740042: 'user6',
        249029217524645889: 'user7',
        240380481563131905: 'user8',
        330535151790718976: 'user9',
        236694472883175426: 'user10',
        203491015808516096: 'user11',
        373033173715517440: 'user12',
        185165742495367168: 'user13',
        194323407431532544: 'user14',
        188483813159075840: 'user15',
        195841061531287552: 'user16',
        197264395196170240: 'user17',
        189339029265842176: 'user18',
        470086166503489536: 'user19',
        218977515404787712: 'user20',
        186276713364324353: 'user21',
        185285433012387840: 'user22',
        211810742003957761: 'user23',
        236682223128936448: 'user24',
        402764753195368448: 'user25',
        264676005933744128: 'user26',
        273347745488699392: 'user27',
        236002193189240833: 'user28',
        732621248395346020: 'user29',
        576284647181254656: 'user30'
    }

meme_dict = {
    'mark': 'https://preview.redd.it/vjm9wz9jymb31.png?width=640&auto=webp&s=47c7c5875da11f07e5fdd9ab61ce3d02a9193105',
    'chicken': 'https://video-syd2-1.xx.fbcdn.net/v/t42.3356-2/95183862_3801944146544171_5579162729793050027_n.mp4/video-1588594638.mp4?_nc_cat=100&_nc_sid=060d78&_nc_ohc=zCVoFSr3AGcAX8On2mQ&vabr=443343&_nc_ht=video-syd2-1.xx&oh=7511cba117866d145742e8944d75bb17&oe=5EB149A2&dl=1',
    'obama': 'https://preview.redd.it/j7z0dk5yqdf31.jpg?width=773&auto=webp&s=864891cd7f95ab225e9d62a912bfc27011ddee36',
    'cat': 'https://preview.redd.it/wrhyk1qe6cm31.jpg?width=500&auto=webp&s=095186a45c539b077092b5672dc63d2f1d9e7bd9',
    'dog': 'https://preview.redd.it/6w2gkixd2bb31.jpg?width=786&auto=webp&s=ec83fcb1ce8d4663f191a2475c04c8ff1de2741e',
    'meme': 'https://preview.redd.it/c4km9r4ditd31.jpg?width=193&auto=webp&s=979a568ab6a0b5a227099c1caf6c4ffd81979ed0',
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UNICODE DICTIONARY CREATER
# Creates a mapping of all unicode characters with their descriptors, used for kpop
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
unicode_dict = {}
for i in range(sys.maxunicode):
    c = chr(i)
    try:
        x = unicodedata.name(c)
        unicode_dict[c] = x
    except:
        pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONFUSABLE LIST CREATOR
# Creates a list of confusable characters for 'k' 'o' and 'p'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
k_regex_str = confusables.confusable_regex('k')
k_regex = regex.compile(k_regex_str)
p_regex_str = confusables.confusable_regex('p')
p_regex = regex.compile(p_regex_str)
o_regex_str = confusables.confusable_regex('o')
o_regex = regex.compile(o_regex_str)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FACEBOOK LOGIN
# Logs in to facebook so that Barney can message the chat about steve stream
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# if __name__ == "__main__":
#     fb_client = fbchat.Client("barneydiscordbot@gmail.com", "112233Qwer")
#     if not fb_client.isLoggedIn():
#         fb_client.login()



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DISCORD CLIENT SETTER
# Techincally a lot of this code, especially the @client.event stuff should be wrapped inside a class, but eh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PERIOD ANNOUNCER
# Used on weekdays to announce period times
# At recess, lunch, and after school, all users in voice channels are moved to the "Green Zone" channel
# At 3:20, all users in voice channels are moved to their corresponding transport
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def period_announcer(self):
    global connected
    await self.wait_until_ready()
    guild = discord.utils.get(self.guilds, id=210716706501296128)
    channel = discord.utils.get(guild.text_channels, id=704836355070361780)
    mention = "@everyone"
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
                            if (user.id == 195841061531287552) and (voice_channel.id != walk_channel.id): #ciaran
                                await user.move_to(walk_channel)
                            if (user.id == 188483813159075840) and (voice_channel.id != boat_channel.id): #jerry
                                await user.move_to(boat_channel)
                        except:
                            continue
                await asyncio.sleep(60)
                continue
            else:
                await asyncio.sleep(2)
            

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# .TXT FILE POPULATOR
# Used to save to any file a json-loadable dictionary of all users of grant's guild, with user IDs as keys, the int 0 as value.
# Checks to see if existing entries for each user exists, otherwise creates a new one
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def txt_populator(txt_file, client, GUILD, roles=False):
    inFile = open(f'txt_files/{txt_file}')
    member_list_str = inFile.read()
    inFile.close()
    try:
        member_list_dict = json.loads(member_list_str)
    except:
        member_list_dict = {}
    for guild in client.guilds:
        if str(guild.id) == GUILD:
            break
    for member in guild.members:
        current_member = member_list_dict.get(str(member.id), False)
        if current_member:
            continue
        else:
            if not roles:
                member_list_dict[str(member.id)] = 0
            else:
                role_list = member.roles
                role_list_ids = []
                for role in role_list:
                    if role in guild.roles:
                        role_list_ids.append(str(role.id))
                role_list_str = ','.join(role_list_ids)
                member_list_dict[str(member.id)] = role_list_str
    outFile = open(f'txt_files/{txt_file}', 'w')
    member_list_str = json.dumps(member_list_dict, indent=4)
    outFile.write(member_list_str)
    outFile.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# THE GLORIOUS KPOP KICKER
# Used to kick any user that has triggered the global kpop_pattern regex
# The user to kick, as well as the channel to invite them back to if they apologise, are required.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def kpop_kicker(channel, target_user):
    try:
        await target_user.create_dm()
        await target_user.dm_channel.send(f'kpop is dumb {target_user.name} don\'t mention it again >:(\nI\'ll send you back an invite if you apologise. I don\'t have all day though, so hurry it up.')
        await channel.guild.kick(target_user)
        def check(m):
            return ('sorry' in m.content.lower() or 'apologies' in m.content.lower() or 'soz' in m.content.lower()) and m.channel == target_user.dm_channel and m.author == target_user
        try:
            msg = await client.wait_for('message', timeout=20.0, check=check)
        except:
            await target_user.dm_channel.send('ok fine buddy ugh ask andrei for an invite fuckin smh')
        else:
            await target_user.dm_channel.send('ok cool, i\'ll let you back in, but don\'t do it again buddy.')
            channel_invite = await channel.create_invite(max_age = 0, max_uses = 1, unique = True, reason='apologised like a big boy')
            await target_user.dm_channel.send(channel_invite.url)
    except Exception as e:
        print(e)
        print(f"User {target_user.name} is not part of Barney's Fun House, must manually receive invite.")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LEAGUE OF LEGENDS KICKER
# Used to kick any user that has triggered the global kpop_pattern regex
# The user to kick, as well as the channel to invite them back to if they apologise, are required.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def league_kicker(channel, target_user):
    # try:
    await target_user.create_dm()
    await target_user.dm_channel.send(f'too much league of legends {target_user.name} \ni\'ll send you back an invite if you apologise. i don\'t have all day though, so hurry it up.')
    await channel.guild.kick(target_user)
    def check(m):
        return ('sorry' in m.content.lower() or 'apologies' in m.content.lower() or 'soz' in m.content.lower()) and m.channel == target_user.dm_channel and m.author == target_user
    try:
        msg = await client.wait_for('message', timeout=20.0, check=check)
    except:
        await target_user.dm_channel.send('ok fine buddy ask someone else for an invite smh')
    else:
        await target_user.dm_channel.send('ok cool, i\'ll let you back in, but don\'t do it again buddy.')
        channel_invite = await channel.create_invite(max_age = 0, max_uses = 1, unique = True, reason='apologised like a big boy')
        await target_user.dm_channel.send(channel_invite.url)
    # except Exception as e:
    #     print(e)
    #     print(f"User {target_user.name} is not part of Barney's Fun House, must manually receive invite.")




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BACKUP KPOP CHECK
# Code that runs in case the main kpop regex fails to find a match
# Deeper search involving unicode data/category lookups
# Also uses the confusables module to access unicode's 'confusables.txt' 
# Any amount of characters after the first k, and then one character
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def backup_kpop_check_phrase_checker(new_index, phrase_list, guild):
    global unicode_dict
    global k_regex, o_regex, p_regex
    k, p1, o, p2 = False, False, False, False
    # if guild:
    #     if guild.id != 210716706501296128:
    #         print(phrase_list)
    index, k_num, p1_num, o_num, p2_num = 0, 0, 0, 0, 0
    # print(f'new phrase list: {phrase_list}')
    for char in phrase_list:
    #     if guild:
    #         if guild.id != 210716706501296128:
    #             print('\n')
    #             print(f'k = {k}, p1 = {p1}, o = {o}, p2 = {p2}')
        try:
            uni_desc = unicode_dict[char]
    #         if guild:
    #             if guild.id != 210716706501296128:
    #                 print(char)
    #                 print(' P ' in uni_desc or uni_desc[:2] == 'P ' or uni_desc[-2:] == ' P' or p_regex.search(char))
    #                 print(uni_desc)
    #                 print(unicodedata.category(char))
    #                 print(f'new_index: {new_index}, index: {index} k_num: {k_num}, p1_num: {p1_num}, o_num: {o_num}, p2_num: {p2_num}')
            if k == True and p1 == True and o == True and p2 == False and (' P ' in uni_desc or uni_desc[:2] == 'P ' or uni_desc[-2:] == ' P' or p_regex.search(char)):
                # if guild:
                    # if guild.id != 210716706501296128:
                        # print(index - o_num)
                whitespace = True
                for x in phrase_list[(o_num - k_num + 1):(index)]:
                    # if guild:
                        # if guild.id != 210716706501296128:
                            # print(unicodedata.category(x))
                    if 'Z' not in unicodedata.category(x) and 'M' not in unicodedata.category(x) and 'C' not in unicodedata.category(x) and x != '\n':
                        whitespace = False
                if ((new_index - o_num) <= 2) or whitespace is True:
                    p2_num = new_index
                    # print('p2')
                    p2 = True
                    break
            elif k == True and p1 == True and o == False and ((' O ' in uni_desc) or (uni_desc[:2] == 'O ') or (uni_desc[-2:] == ' O') or emoji_regex.search(char) or o_regex.search(char)):
                # print(index - p1_num)
                whitespace = True
                for x in phrase_list[(p1_num - k_num + 1):(index)]:
                    if 'Z' not in unicodedata.category(x) and 'M' not in unicodedata.category(x) and 'C' not in unicodedata.category(x) and x != '\n':
                        whitespace = False
                if ((new_index - p1_num) <= 2) or whitespace is True:
                    # print('o')
                    o_num = new_index
                    index += 1
                    new_index += 1
                    o = True
            elif k == True and p1 == False and (' P ' in uni_desc or uni_desc[:2] == 'P ' or uni_desc[-2:] == ' P' or p_regex.search(char)):
                # print('p1')
                whitespace = True
    #             print(phrase_list[((k_num - k_num) + 1):(index)])
                for x in phrase_list[(k_num - k_num + 1):(index)]:
    #                 print(f'char: {x}, cat: {unicodedata.category(x)}')
                    if 'Z' not in unicodedata.category(x) and 'M' not in unicodedata.category(x) and 'C' not in unicodedata.category(x) and x != '\n':
    #                     print(f'whitespace false with character{x}')
                        whitespace = False
    #                 print('\n')
                if ((new_index - k_num) <= 2) or whitespace is True:
                    p1 = True
                    p1_num = new_index
                    index += 1
                    new_index += 1
            elif k == False and (' K ' in uni_desc or uni_desc[:2] == 'K ' or uni_desc[-2:] == ' K' or k_regex.search(char)):
                # print('k')
                k = True
                k_num = new_index
                index += 1
                new_index += 1
            else:
                new_index += 1
                index += 1
                continue
        except:
            index += 1
            new_index += 1
            continue
        
    if k and p1 and o and p2:
        return True, k_num, p1_num, o_num, p2_num
    else:
        return False, None, None, None, None

async def backup_kpop_check(phrase, user, guild, nick=False, message=False, custom_response=False, kick=True):
    # print('backup kpop check')
    global unicode_dict
    global k_regex, o_regex, p_regex
    success = False
    phrase_list = list(phrase)
    # if guild:
    #     if guild.id != 210716706501296128:
    #         print(phrase_list)
    index, k_num, p1_num, o_num, p2_num = 0, 0, 0, 0, 0
    for char in phrase_list:
        try:
            uni_desc = unicode_dict[char]
            # if guild:
                # if guild.id != 210716706501296128:
                    # print(uni_desc)
                    # print(unicodedata.category(char))
                    # print(f'index: {index}, k_num: {k_num}, p1_num: {p1_num}, o_num: {o_num}, p2_num: {p2_num}')
            if ' K ' in uni_desc or uni_desc[:2] == 'K ' or uni_desc[-2:] == ' K' or k_regex.search(char):
    #             print('k')
    #             print(f'k detected at index {index}')
                success, k_num, p1_num, o_num, p2_num = await backup_kpop_check_phrase_checker(index, phrase_list[index:], guild)
    #             print(success)
                if success:
                    break
                index += 1
            else:
                index += 1
                continue
        except:
            index += 1
            continue
    
    if success:
        if message:
            phrase_list[p2_num] = f' __***{phrase[p2_num].upper()}***__ '
            phrase_list[o_num] = f' __***{phrase[o_num].upper()}***__ '
            phrase_list[p1_num] = f' __***{phrase[p1_num].upper()}***__ '
            phrase_list[k_num] = f' __***{phrase[k_num].upper()}***__ '
            response = ''.join(phrase_list)
            await message.channel.send(f'you just wrote {response} buddy i see right through you')
            target_channel = message.channel
        elif nick:
            target_channel = guild.text_channels[0]
            await target_channel.send(f'come on {user.mention} i can read ur name buddy im not blind')
        elif custom_response:
            target_channel = guild.text_channels[0]
            await target_channel.send(f'{custom_response}')
        
        if kick:
            await kpop_kicker(target_channel, user)
        else:
            return True
    else:
        return None





# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# T H E     M A F I A      C O D E
# The following functions are all used for the currently almost-functional-but-not-quite-there-yet-due-to-random-bugs-at-the-very-end-of-the-game-
# that-i-cant-be-assed-to-properly-debug Mafia function.
# CURRENT BUGS INCLUDE: idk add something to this when ur bothered to test it again ok thanks andrei love you xx
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~


# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# ROLE DECIDER
# used to assign random roles to players.
# 1 detective, 1 medic, one third of the players rounded up are mafia, rest are innocents
# Potential for modularity to add roles based on keywords in mafia game creation???
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
def role_decider(players):
    player_roles = {}
    mafia_list = []
    mafia_quantity = math.ceil(len(players)/3)
    innocent_quantity = mafia_quantity - 1 - 1
    while mafia_quantity > 0:
        i = players.pop(random.randint(0, (len(players)-1)))
        player_roles[i] = "Mafia"
        mafia_list.append(i)
        mafia_quantity -= 1
        continue
    player_roles[players.pop(random.randint(0, (len(players)-1)))] = "Detective"
    player_roles[players.pop(random.randint(0, (len(players)-1)))] = "Medic"
    for player in players:
        player_roles[player] = "Innocent"
    return player_roles, mafia_list


# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# ROLE DESCRIPTION CREATOR
# Generates descriptions for each role, returned to main mafia code and sent to each user via DM
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
def role_description(role):
    if role == "Mafia":
        response = "Your goal is to kill all players that are not in the mafia. You achieve this by, as a group, voting for someone to kill during the night.\nIf at least one member of the mafia evades capture and is the last to be alive, the entire Mafia team wins.\nYour vote on who to kill each night must be unanimous, or no action will be taken."
    elif role == "Detective":
        response = "Each night you are able to ask Barney if a single player is part of the mafia, to which Barney will respond yes or no."
    elif role == "Medic":
        response = "Each night you are able to choose a person to \'heal\'.\nIf the mafia chooses your chosen person to kill, they will not die."
    elif role == "Innocent":
        response = "You don't get to do anything special, sorry!"
    return response

# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# MAFIA PERMISSIONS CREATOR
# Gives each player with the Mafia role the necessary permissions to interact with the Mafia text channel
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
def mafia_permissions_creator(mafia_list):
    mafia_permissions = {}
    for mafia in mafia_list:
        mafia_permissions[mafia] = discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True)
    return mafia_permissions

# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# VOTE MESSAGE CREATOR
# Used to generate and send a message to any text channel in which they can vote for a specific player using an emoji player dictionary
# CURRENT BUGS: Does not always work properly for detective: detective votes for one player but returned another. investigation is correct, but correct player is not investigated
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
async def vote_message_creator(player_roles, client, channel, mafia=False, medic=False, detective=False):
    emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '😂', '😍', '🥵', '😱', '🤡']
    vote_dict = {}
    for player in player_roles.keys():
        if player == client.user:
            continue
        if mafia:
            if player_roles[player] == 'Mafia':
                continue
        if medic:
            if player_roles[player] == 'Medic':
                continue
        if detective:
            if player_roles[player] == 'Detective':
                continue
        vote_dict[emoji_list.pop(0)] = player
    player_emoji_string = ''
    for emoji in vote_dict.keys():
        player_emoji_string = f'{player_emoji_string}{emoji} - {vote_dict[emoji].name}\n'
    if mafia:
        x = 'Vote unanimously for someone to kill by reacting to this message with the corresponding emoji. You have 20 seconds.'
        vote_time = 20
    elif medic:
        x = 'Vote for somebody to save. If the mafia has chosen that player to die, they will instead survive. You have 15 seconds.'
        vote_time = 15
    elif detective:
        x = 'Vote for somebody to investigate. You will receive a message on whether that player is part of the mafia. You have 15 seconds.'
        vote_time = 15
    else:
        x = 'Vote for somebody to lynch out of the game. If a player has a majority of the votes, they will be lynched. In the event of a tie, there will be a revote with only those players. You have two minutes.'
        vote_time = 15
    vote_message = await channel.send(f'{x}\n{player_emoji_string}')
    for emoji in vote_dict.keys():
        await vote_message.add_reaction(emoji)
    return vote_message, vote_time, vote_dict

# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
# Very very very basic wake up message creator.
# Medic response has wayy too much info fix that pls
# ~~~~~M~A~F~I~A~~~~~C~O~D~E~~~~~
def wake_up_message_creator(player_roles, victim, saved_player, medic_player):
    if victim:
        death_responses = [
            f'{victim.name} died. Unlucky.',
            f'{victim.name} died. Super unlucky.'
        ]
        saved_responses = [
            f'{victim.name} was about to die, but {medic_player.name} saved them. Lucky.',
            f'{victim.name} was about to die, but {medic_player.name} saved them. Super lucky.'
        ]
    if not victim:
        message = 'No one died.'
        killed_player = None
    elif victim == saved_player:
        message = random.choice(saved_responses)
        killed_player = None
    else:
        message = random.choice(death_responses)
        killed_player = victim
    return message, player_roles, killed_player





# Used to always run the Period Announcer function in the background

# client.bg_task = client.loop.create_task(period_announcer(client))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON READY (on barney's connection to discord)
# connected stops the period announcer from happening more than once i think??? not 100% sure but i don't think it works
# because connected is changed to false usually while period_announcer is asyncio sleeping so while loop is not broken
# Populates all text files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_ready():
    global connected
    global current_time
    connected = False
    print(f'{client.user.name} has connected to Discord.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"))
    txt_populator('swear_count.txt', client, GUILD)
    txt_populator('im_feeling_lucky.txt', client, GUILD)
    txt_populator('roles_list.txt', client, GUILD, roles=True)
    txt_populator('val_encrypted_details.txt', client, GUILD)
    txt_populator('val_shop_details.txt', client, GUILD)
    print(f'It took {time.time()-current_time} seconds to boot up')
    connected = True




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON MEMBER JOIN (new user joins guild)
# gives default roles = blue, school id
# if user was previously on the server, *eventually* gives them back their roles right before they left (or were kicked for saying the k word)
# might take a while because of rate limiting? either way, if barney is offline when someone rejoins they don't get roles so they're gonna bug you have fun
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome loser to the cool kids server'
    )
    dong_guild = member.guild
    role_id_blue = 232788103948009472
    role_id_orange = 234552386784329728
    role_id_school_id = 691788291250454598
    blue_role = discord.utils.get(dong_guild.roles, id=role_id_blue)
    school_id_role = discord.utils.get(dong_guild.roles, id=role_id_school_id)
    inFile = open('txt_files/roles_list.txt', 'r')
    member_list_str = inFile.read()
    inFile.close()
    member_list_dict = json.loads(member_list_str)
    if str(member.id) in member_list_dict.keys():
        member_roles_id_str = member_list_dict[str(member.id)]
        #print(member_roles_id_str)
        member_roles_id_list = member_roles_id_str.split(',')
        #print(member_roles_id_list)
        member_roles_id_list.pop(0)
        guild_roles = dong_guild.roles
        guild_roles_id = []
        for role in guild_roles:
            guild_roles_id.append(role.id)
        #print(guild_roles_id)
        for role_id in member_roles_id_list:
            #print(role_id)
            if int(role_id) in guild_roles_id:
                role = dong_guild.get_role(int(role_id))
                #print(role)
                if role:
                    await member.add_roles(role)
                    #print('success')
                else:
                    print(f'role "{role.name}" not added')
    else:
        await member.add_roles(blue_role)
        await member.add_roles(school_id_role)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON MEMBER REMOVE (user leaving the guild)
# user's roles are updated to their role dictionary, so that the correct roles are given upon them rejoining
# implemented after gnu abused the system to get roles back that were saved when barney initialised by leaving and rejoining, even if they were stripped away by another user
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_member_remove(member):
    inFile = open('txt_files/roles_list.txt')
    member_list_str = inFile.read()
    inFile.close()
    member_list_dict = json.loads(member_list_str)
    for member_id in member_list_dict.keys():
        if int(member_id) == member.id:
            role_list = member.roles
            role_list_ids = []
            dong_guild = member.guild
            for role in role_list:
                if role in dong_guild.roles:
                    print(role.name)
                    role_list_ids.append(str(role.id))
            role_list_str = ','.join(role_list_ids)
            member_list_dict[str(member.id)] = role_list_str
    outFile = open('txt_files/roles_list.txt', 'w')
    member_list_str = json.dumps(member_list_dict)
    outFile.write(member_list_str)
    outFile.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON MEMBER UPDATE (if any user literally does anything e.g. status change, nickname update etc.)
# So far, only used to check if a nickname was changed to kpop, and to see who did it
# utilises AUDIT LOGS for this, docs are kinda unepic, use the debug console it's more helpful imo
# Also does a check to make sure nobody's been playing league of legends for too long >:(
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_member_update(before, after):

    if (before.id == 203672102509740042):
        # print("swag")
        pass
    

    if after.activity is not None and league_detection:
        success = True
        if before.activity is None:
            pass
        elif (before.activity.name == after.activity.name):
            success = False

        if after.activity.name.lower() == "league of legends" and success and after.id not in league_players:
            id = after.id
            league_players.append(id)
            # await after.create_dm()
            await after.send("you\'ve got one hour of league time on the clock buddy, after that you\'re out of the server")
            await asyncio.sleep(3600)
            print("hi")
            new_member = after.guild.get_member(id)

            if new_member.activity is None:
                league_players.remove(id)
            elif new_member.activity.name.lower() != "league of legends":
                league_players.remove(id)
            else:
                # await after.create_dm()
                await after.send("five minutes left, tick tock")
                await asyncio.sleep(300)
                new_member = after.guild.get_member(id)
                
                if new_member.activity is None:
                    league_players.remove(id)
                elif new_member.activity.name.lower() != "league of legends":
                    league_players.remove(id)
                else:
                    channel = after.guild.text_channels[0]
                    await league_kicker(channel, after)


    n = after.nick
    if before.nick == n:
        pass
    else:
        kpop_pattern = regex.compile(r"((k[^ ]*[pP][o0O][pP])|(korean pop)|(([κkk长K<])|(l𡿨)|(\|<)|(/<)|(:regional_indicator_k:)|(\)<))[.,/'\"%^&*?!@’#$()-_+=~`|<> ]*(([م尸ρ卩pمрРP])|(:parking:)|(:regional_indicator_p:))[.,/'\"%^&’*?!@#$()-_+=~`|<> ]*(([םo口õο๐σ〇θôōøоО٥סּ0O])|(:regional_indicator_o:))[.,/'\"%^&*?!@#’$()-_+=~`|<> ]*(([م尸ρ卩pمрРP])|(:parking:)|(:regional_indicator_p:)))")
        guild = before.guild

        if n:
            immune = False
            if kpop_pattern.search(n):
                print('kpop detected in username change')
                async for entry in guild.audit_logs(limit=1):
                    if entry.target == entry.user:
                        
                        kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                        if str(entry.user.id) in kpop_coupons_users.keys():
                            if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                immune = True
                            elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                del kpop_coupons_users[str(entry.user.id)]
                                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                outFile.write(json.dumps(kpop_coupons_users))
                                outFile.close()

                        response = f'i saw you change your nickname to the k word {entry.user.mention} how dumb do you think i am'
                    elif entry.target != entry.user:
                        
                        kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                        immunity_str = ''
                        if str(entry.user.id) in kpop_coupons_users.keys():
                            if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                immune = True
                                immunity_str = '. i can\'t kick you bc you have the kpop pass, but don\'t dog someone else out smh.'
                            elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                del kpop_coupons_users[str(entry.user.id)]
                                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                outFile.write(json.dumps(kpop_coupons_users))
                                outFile.close()

                        response = f'i saw you {entry.user.mention} change {entry.target.mention}\'s nickname to the k word you really gonna do them like that{immunity_str}'
                target_channel = guild.text_channels[0]
                await target_channel.send(response)
                if not immune:
                    await kpop_kicker(target_channel, entry.user)
            else:
                async for entry in guild.audit_logs(limit=1):
                    if entry.target == entry.user:

                        kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                        if str(entry.user.id) in kpop_coupons_users.keys():
                            if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                immune = True
                            elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                del kpop_coupons_users[str(entry.user.id)]
                                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                outFile.write(json.dumps(kpop_coupons_users))
                                outFile.close()

                        response = f'i saw you change your nickname to the k word {entry.user.mention} how dumb do you think i am'
                    elif entry.target != entry.user:
                        
                        kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                        immunity_str = ''
                        if str(entry.user.id) in kpop_coupons_users.keys():
                            if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                immune = True
                                immunity_str = '. i can\'t kick you bc you have the kpop pass, but don\'t dog someone else out smh.'
                            elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                del kpop_coupons_users[str(entry.user.id)]
                                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                outFile.write(json.dumps(kpop_coupons_users))
                                outFile.close()

                        response = f'i saw you {entry.user.mention} change {entry.target.mention}\'s nickname to the k word you really gonna do them like that{immunity_str}'
                success = await backup_kpop_check(n, entry.user, guild, nick=False, message=False, custom_response=False, kick=False)
                if success is True:
                    async for entry in guild.audit_logs(limit=1):
                        if entry.target == entry.user:
                            
                            kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                            if str(entry.user.id) in kpop_coupons_users.keys():
                                if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                    immune = True
                                elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                    del kpop_coupons_users[str(entry.user.id)]
                                    outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                    outFile.write(json.dumps(kpop_coupons_users))
                                    outFile.close()

                            response = f'i saw you change your nickname to the k word {entry.user.mention} how dumb do you think i am'
                        elif entry.target != entry.user:

                            kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                            immunity_str = ''
                            if str(entry.user.id) in kpop_coupons_users.keys():
                                if kpop_coupons_users[str(entry.user.id)] >= int(time.time()):
                                    immune = True
                                    immunity_str = '. i can\'t kick you bc you have the kpop pass, but don\'t dog someone else out smh.'
                                elif kpop_coupons_users[str(entry.user.id)] < int(time.time()):
                                    del kpop_coupons_users[str(entry.user.id)]
                                    outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                                    outFile.write(json.dumps(kpop_coupons_users))
                                    outFile.close()

                            response = f'i saw you {entry.user.mention} change {entry.target.mention}\'s nickname to the k word you really gonna do them like that'
                    target_channel = guild.text_channels[0]
                    await target_channel.send(response)
                    await kpop_kicker(target_channel, entry.user)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON VOICE STATE UPDATE
# Currently being used to send an @here notification when Steven starts streaming a game
# Can also potentially be used down the line for Schmalex voice recognition to auto start when he joins?
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# @client.event
# async def on_voice_state_update(member, before, after):
#     global steve_stream
#     now = datetime.datetime.now()
#     if member.id == 183880246917988353: # Steven
#         if steve_stream:
#             inFile = open('txt_files/steve_stream_time.txt')
#             time_str = inFile.read()
#             steve_time = float(time_str)
#             if time.time() - steve_time >= 18000:
#                 steve_stream = False
# 
#         if after.self_stream and (not before.self_stream) and (now.hour >= 22) and (not steve_stream):
#             try:
#                 if 'overwatch' not in member.activity.name.lower():
#                     steve_stream = True
#                     current_time = time.time()
#                     outFile = open('txt_files/steve_stream_time.txt', 'w')
#                     outFile.write(str(current_time))
#                     outFile.close()
#                     text_channel = after.channel.guild.text_channels[0]
#                     await text_channel.send('@everyone steve stream has just started!')
#                     if not fb_client.isLoggedIn():
#                         fb_client.login()
#                     msg = f'hi guys steve stream has started'
#                     fb_client.send(fbchat.Message(text=msg), thread_id=2654775107962874, thread_type=fbchat.ThreadType.GROUP)
#             except Exception as e:
#                 print(e)
#                 return None




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GENERAL FUCKERY
# Use this for anything relatively simple, where barney just sends a one liner in response to a specific message and no other code should be run
# Barney's humble beginnings, barney_response 1 2 and 3 were his first responses along with greeting_pattern.
# Oh how my boy has grown, brings a tear to my eye ;(
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def general_fuckery(message):
    msg = message.content.lower()
    global user_dict
    global meme_dict

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

    greeting_pattern = regex.compile('(^hi(?!( barney)) .*)|(^hello.*)|(^hey.*)|(^howdy.*)|(^obi wan)')

    if msg == 'barney':
        response = random.choice(barney_response_1)
        return response

    elif msg == 'fuck you barney':
        response = barney_response_2
        return response

    elif 'hi barney' in msg:
        try:
            response = f'hi {user_dict[message.author.id]}'
        except:
            response = 'hi'
        return response

    elif greeting_pattern.search(msg):
        response = barney_response_3
        return response
    
    elif 'mr 305' in msg: # ok ciaran
        response = 'mr worldwide'
        return response
    

    elif '🤣' in msg:
        response = ':rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: THAT WAS FUNNY!!! :rofl: :rofl: :rofl: :rofl: :rofl: :rofl: :rofl:'
        return response

    elif 'gn ' in msg or 'good night' in msg:
        response = 'sleep tight king'
        return response
    
    elif msg in meme_dict.keys():
        response = meme_dict[msg]
        return response
    
    else:
        mock_chance = random.randint(1, 30)
        if mock_chance == 1:
            received_message = msg
            new_letters = []
            for index, letter in enumerate(received_message):
                if index % 2 == 0:
                    if letter == 'l':
                        new_letters.append(letter.upper())
                    else:
                        new_letters.append(letter)
                else:
                    if letter == 'i':
                        new_letters.append(letter)
                    else:
                        new_letters.append(letter.upper())
            response = ''.join(new_letters)
        else:
            response = None
#        e_count = 0
#        for i in new_message.lower():
#            if i == 'e':
#                e_count += 1
#        
#        response = (f'{response}\nAlso there were {str(e_count)} E\'s in that message.')
        return response


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SWEAR PARSER
# Used to track the amount of times a user has sworn, as well as an epic funny response if the amount contains the sex number!
# also contains a few user specific responses, for that extra personal touch
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def swear_parser(message, swear_instances):
    global user_dict

    inFile = open('txt_files/swear_count.txt')
    swear_count_str = inFile.read()
    inFile.close()
    swear_count_dict = json.loads(swear_count_str)

    author_id = message.author.id
    swear_number = int(swear_count_dict[str(author_id)])
    swear_number += swear_instances
    swear_count_dict[author_id] = swear_number

    outFile = open('txt_files/swear_count.txt', 'w')
    swear_count_str = json.dumps(swear_count_dict)
    outFile.write(swear_count_str)
    outFile.close()

    author = str(message.author)
    author = author[:-5]
    if swear_number == 1:
        response = f'This is your first time swearing, {author}. I\'ll let you off with a warning this time, but don\'t let me catch you doing it again.'
    elif swear_number == 2:
        response = f'What did I just say to you {author}. It\'s not that hard to not swear mate.'
    elif swear_number == 3:
        response = f'OK that\'s it. I give up. Do what you want with your life, i\'m not your bloody mother, though wherever she is I can feel her disappointment in you.'
    elif '69' in str(swear_number):
        response = f'hahahahah you have {swear_number} swears 69 lol'
    else:
        if message.author.id in user_dict.keys():
            name = user_dict[message.author.id]
        else:
            name = message.author.name
        response = f'{swear_number} swears aren\'t you cool *{name}*'#f'You\'ve sworn {str(swear_number)} times now. I hope you\'re happy with yourself.'

    return response


def entitify(text):
    return ''.join('&#%d;' % ord(c) for c in text)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# KPOP QR CREATOR
# Module used to create a kpop coupon code for any user
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def kpop_qr_creator(template, return_file=False):
    global user_dict
    kpop_code = secrets.token_urlsafe(16)
    print(f'kpop_code: {kpop_code}')
    kpop_coupons = json.loads(open('txt_files/kpop_coupons.txt').read())
    kpop_coupons['unused'][kpop_code] = template
    outFile = open('txt_files/kpop_coupons.txt', 'w')
    outFile.write(json.dumps(kpop_coupons))
    outFile.close()
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_Q,
        box_size=7,
        border=0
    )
    qr.add_data(kpop_code)
    qr.make(fit=True)

    qr_image = qr.make_image()
    qr_w, qr_h = qr_image.size
    print(f'width: {qr_w}, height: {qr_h}')
    template = Image.open(f'qr_codes/templates/{template}.png', 'r')
    template.paste(qr_image, (846, 368))
    file_name = f'qr_codes/{int(time.time())}.png'
    template.save(file_name)
    if not return_file:
        return f'A {template} coupon was created with code {kpop_code}'
    else:
        return file_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# KPOP COUPON REDEEMER
# Checks/redeems kpop coupon codes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def kpop_coupon_redeemer(image, user):
    global user_dict
    decode = pyzbar.decode(image)
    if not decode:
        return None
    else:
        kpop_coupons = json.loads(open('txt_files/kpop_coupons.txt').read())
        coupon_code = str(decode[0][0])[2:-1]
        print(coupon_code)
        print(kpop_coupons['unused'].keys())
        if coupon_code in kpop_coupons['used']:
            return 'this coupon has been used before, get your own code.'
        elif coupon_code in kpop_coupons['unused'].keys():
            if user.id == 183880560454664192: # grant
                return 'you can\'t redeem coupons grant u can already say it as much as you want'
            else:
                kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                expiry = kpop_coupons['unused'][coupon_code]
                if expiry == '24_hours':
                    expiry_time, expiry_str = int(time.time() + 86400), '24 hours'
                elif expiry == '3_days':
                    expiry_time, expiry_str = int(time.time() + 259200), '3 days'
                elif expiry == '7_days':
                    expiry_time, expiry_str = int(time.time() + 604800), '7 days'
                kpop_coupons_users[user.id] = expiry_time
                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                outFile.write(json.dumps(kpop_coupons_users))
                outFile.close()
                
                kpop_coupons['used'].append(coupon_code)
                del kpop_coupons['unused'][coupon_code]
                outFile = open('txt_files/kpop_coupons.txt', 'w')
                outFile.write(json.dumps(kpop_coupons))
                outFile.close()

                if user.id in user_dict.keys():
                    user = user_dict[user.id]
                else:
                    user = user.name
                return f'hi {user}, i\'ve redeemed your kpop coupon that expires in {expiry_str}. go nuts kiddo'
        else:
            return f'i didn\'t recognise that coupon, try again'



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BLOCK LETTER CREATOR
# converts any string of characters into discord's emoji equivalent, as it contains emojis for each english letter and arabic numeral
# messages cannot be over 2000 characters, hence the fail safe
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def block_letter_creator(phrase):
    num_words = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
    new_phrase_list = []
    non_block = 0
    for i in phrase:
        if i in "0123456789":
            new_phrase_list.append(f":{num_words[int(i)]}:")
        elif i in "abcdefghijklmnopqrstuvwxyz":
            new_phrase_list.append(f':regional_indicator_{i}:')
        elif i == ' ':
            new_phrase_list.append('      ')
        else:
            new_phrase_list.append(i)
            non_block += 1
    new_phrase = ' '.join(new_phrase_list)
    if non_block == len(phrase):
        return 'that message didn\'t have any valid block letters'
    elif len(new_phrase) >= 2000:
        return 'that message was too long for me to convert into block letters'
    else:
        return new_phrase


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VOICE RECEIVE CONTROLLER
# Controls starting the JS in charge of listening to a user
# Also does all the audio conversion
# Sends the audio to wit.ai for processing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def voice_receive_controller(user_id, channel_id, message):
    global receive_connections
    global receive_users
    global listeners_active
    global token_js_dict
    global whos_listening_to_who

    final_str = ''

    receive_connections += 1
    active_bot = 0 + receive_connections
    if receive_connections > 3:
        await message.channel.send('i don\'t have any more helpers that can listen in on people')
        return None
    if user_id in receive_users:
        await message.channel.send('already listening to that user')
        return None
    receive_users.append(user_id)
    whos_listening_to_who[message.author.id] = user_id

    wit_token = token_js_dict[active_bot][0]
    js_file = token_js_dict[active_bot][1]
    listeners_active[message.author.id] = active_bot

    url = 'https://api.wit.ai/speech?v=20200716'
    header = {
        'Authorization': f'Bearer {wit_token}',
        'Content-Type': 'audio/wav'
    }

    js_process = subprocess.Popen(['node', js_file, '-c', str(channel_id), '-u', str(user_id)])

    i = 1
    base_path = os.path.join('user_audio_recordings', f'{user_id}')

    if os.path.isdir(base_path):
        pass
    else:
        os.mkdir(base_path)
        record_path = os.path.join(base_path, 'recordings')
        os.mkdir(record_path)
        complete_path = os.path.join(base_path, 'completed')
        os.mkdir(complete_path)
        convert_path = os.path.join(base_path, 'converted')
        os.mkdir(convert_path)


    while listeners_active[message.author.id]:
        while True:
            try:
                complete = open(f'{base_path}/completed/completed_{i}', 'r')
                complete.close()
                break
            except:
                time.sleep(0.5)
                continue
        try:
            file_name = f'{user_id}_{i}'
            subprocess.Popen(['ffmpeg', '-f', 's16le', '-ar', '96.0k', '-ac', '1', '-i', f'{base_path}\\recordings\\{file_name}', f'{base_path}\\converted\\{file_name}.wav'])
            f = open(f'{base_path}/converted/{file_name}.wav', 'rb')
            data = f.read()
            resp = requests.post(url, data=data, headers=header) #wit_client.speech(f, {'Content-Type': 'audio/wav'})
            print(json.loads(resp.text)["text"])
            final_str += f'{json.loads(resp.text)["text"]}\n'
            os.remove(f'{base_path}/completed/completed_{i}')
            os.remove(f'{base_path}/recordings/{file_name}')
            os.remove(f'{base_path}/converted/{file_name}.wav')
            i += 1
        except Exception as e:
            print(e)
            i += 1
    js_process.terminate()
    outFile = open(f'user_audio_recordings/transcripts/{user_id}.txt', 'w')
    outFile.write(final_str)
    outFile.close()



async def voice_receive_leave(message):
    global receive_connections
    global receive_users
    global listeners_active
    global token_js_dict
    global whos_listening_to_who

    user_id = whos_listening_to_who[message.author.id]

    receive_connections -= 1
    active_bot = 0 + receive_connections

    if message.author.id not in listeners_active.keys():
        await message.channel.send('you have not requested to listen to anyone')
        return None
    
    bot_name = token_js_dict[listens_active[message.author.id]][2]
    listeners_active[message.author.id] = None
    await message.channel.send(f'attempting to disconnect {bot_name}. it\'ll take at most 15 seconds, then i\'ll send a txt file transcript.')

    filename = f'user_audio_recordings/transcripts/{user_id}.txt'
    receive_users.remove(user_id)
    del whos_listening_to_who[message.author.id]
    return filename



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VOICE JOINER (proud of this one :) )
# Allows barney to join a voice channel and play an mp3 file from ./audio_files/
# Assumes that the file name given is valid, as that is validated by the on_message code
# voice_cooldown stops another file from being played while barney is already in a voice channel
# enforces a 15 second cooldown per user to stop the piece of shit annoying spammers and to spare my bandwidth at least slightly
# appends to the user_voice_cooldown dictionary so that users are notified of how much longer until their cooldown is expired
# requires ffmpeg to be locally installed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def voice_joiner(message, client, file_names):
    global voice_cooldown
    global user_voice_cooldown
    global user_cooldown_time_remaining
    if voice_cooldown:
        await message.channel.send("wait before you make me join a chat again")
    else:
        try:
            if user_voice_cooldown[message.author.id]:
                await message.channel.send(f"stop abusing me {message.author.display_name}, wait another {round(user_cooldown_time_remaining[message.author.id] - time.time(), 1)} seconds")
        except:
            user = message.author
            try:
                voice_channel = user.voice.channel
            except:
                voice_channel = None
            if voice_channel != None:
                user_voice_cooldown[message.author.id] = True
                voice_cooldown = True
                voice_chance = random.randint(1, len(file_names))
                file_name = file_names[(voice_chance-1)]
                vc = await user.voice.channel.connect()
                voice = discord.utils.get(client.voice_clients, guild=message.guild)
                source = FFmpegPCMAudio(f"audio_files/{file_name}")
                voice.play(source)
                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await vc.disconnect()
                voice_cooldown = False
                user_cooldown_time_remaining[message.author.id] = time.time() + 15
                await asyncio.sleep(15)
                del user_cooldown_time_remaining[message.author.id]
                del user_voice_cooldown[message.author.id]
            else:
                await message.channel.send("you must be in a voice channel to make me speak")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IM FEELING LUCKY
# A discontinued gambling game, in which users can gamble to increase their role or decrease it/get banned???
# i don't actually know what this is but could be a decent concept???
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def im_feeling_lucky(message):
    inFile = open('im_feeling_lucky.txt')
    swear_count_str = inFile.read()
    inFile.close()
    swear_count_dict = json.loads(swear_count_str)

    author_id = message.author.id    
"""





# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# EQUATION FORMATTER
# Formats the given equation into a variety of readable formats, either for humans, desmos, or sympy.
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
def eqn_formatter(eqn, desmos=False, maths=False, string=False, der=False, double_der=False):
    if desmos:
        if 'sin^-1(' in eqn or 'asin(' in eqn:
            eqn = eqn.replace('sin^-1', r'\\arcsin')
        if 'cos^-1(' in eqn or 'acos(' in eqn:
            eqn = eqn.replace('cos^-1', r'\\arccos')
        if 'tan^-1(' in eqn or 'atan(' in eqn:
            eqn = eqn.replace('tan^-1', r'\\arctan')
        if 'sin' in eqn:
            eqn = eqn.replace('sin', r'\\sin')
        if 'cos' in eqn:
            eqn = eqn.replace('cos', r'\\cos')
        if 'tan' in eqn:
            eqn = eqn.replace('tan', r'\\tan')
        if 'E' in eqn:
            eqn = eqn.replace('E', 'e')
        if 'pi' in eqn:
            eqn = eqn.replace('pi', r'\\pi')
        if '**' in eqn:
            eqn = eqn.replace('**', '^')
        if 'sqrt(' in eqn:
            eqn = eqn.replace('sqrt(', r'\\sqrt(')
        if 'abs(' in eqn:
            eqn = eqn.replace('sqrt(', r'\\abs(')
        if 'y=' not in eqn:
            eqn = f'y={eqn}'
    if maths:
        if 'sin^-1(' in eqn:
            eqn = eqn.replace('sin^-1', 'asin')
        if 'cos^-1(' in eqn:
            eqn = eqn.replace('cos^-1', 'acos')
        if 'tan^-1(' in eqn:
            eqn = eqn.replace('tan^-1', 'atan')
        if 'e' in eqn:
            eqn = eqn.replace('e', 'E')
        if 'pi' in eqn:
            eqn = eqn.replace('e', 'pi')
        if '^' in eqn:
            eqn = eqn.replace('^', '**')
        if 'y=' in eqn:
            eqn = eqn.replace('y=', '')
    if string:
        eqn = str(eqn)
        if 'asin(' in eqn:
            eqn = eqn.replace('asin', 'sin^-1')
        if 'acos(' in eqn:
            eqn = eqn.replace('acos', 'cos^-1')
        if 'atan' in eqn:
            eqn = eqn.replace('atan', 'tan^-1')
        if 'E' in eqn:
            eqn = eqn.replace('E', 'e')
        if '**' in eqn:
            eqn = eqn.replace('**', '^')
        if '-' in eqn:
            eqn = eqn.replace('-', '–')
        if 'y=' not in eqn:
            if der:
                y = "y'"
            if double_der:
                y = "y''"
            eqn = f'{y}={eqn}'
    return eqn

# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# DESMOS HTML CREATOR
# Uses a template html file, "template.html", in order to output an html file with necessary html and javascript data for the graph
# Looks disgusting, but hey it works.
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
def desmos_html_creator(desmos_eqn, eqn_str, eqn_values, desmos_der, der_values, desmos_double_der, double_der_values, eqn_asymptotes, der_asymptotes, double_der_asymptotes):
    eqn_xvals_table = ['<th class="tg-0lax">x</th>']
    eqn_yvals_table = ['<th class="tg-0lax">y</th>']
    der_xvals_table = ['<th class="tg-0lax">x</th>']
    der_yvals_table = ['<th class="tg-0lax">y\'</th>']
    double_der_xvals_table = ['<th class="tg-0lax">x</th>']
    double_der_yvals_table = ['<th class="tg-0lax">y\'\'</th>']


    for x, y in eqn_values.items():
        eqn_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        eqn_yvals_table.append(f'<th class="tg-0lax">{y}</th>')
    for x, y in der_values.items():
        der_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        der_yvals_table.append(f'<th class="tg-0lax">{y}</th>')
    for x, y in double_der_values.items():
        double_der_xvals_table.append(f'<th class="tg-0lax">{x}</th>')
        double_der_yvals_table.append(f'<th class="tg-0lax">{y}</th>')


    x_values_table_str = '\n			'.join(eqn_xvals_table)
    y_values_table_str = '\n			'.join(eqn_yvals_table)
    der_xvals_table_str = '\n			'.join(der_xvals_table)
    der_yvals_table_str = '\n			'.join(der_yvals_table)
    double_der_xvals_table_str = '\n			'.join(double_der_xvals_table)
    double_der_yvals_table_str = '\n			'.join(double_der_yvals_table)

    inFile = open('template.html')
    html = inFile.read()
    inFile.close()

    curves = []
    eqn_limits = []
    der_limits = []
    double_der_limits = []
    curves.append(f"calculator.setExpression({{ id: 'original', latex: '{desmos_eqn}', lineStyle: Desmos.Styles.SOLID }});")
    curves.append(f"calculator.setExpression({{ id: 'derivative', latex: '{desmos_der}', lineStyle: Desmos.Styles.SOLID }});")
    curves.append(f"calculator.setExpression({{ id: 'double-derivative', latex: '{desmos_double_der}', lineStyle: Desmos.Styles.SOLID }});")


    h_eqn_asymp = eqn_asymptotes['h']
    v_eqn_asymp = eqn_asymptotes['v']
    if h_eqn_asymp['oo'][0] != 'oo' and h_eqn_asymp['oo'][0] != '-oo':
        curves.append(f"calculator.setExpression({{ id: 'h_asymp_1', latex: 'y={h_eqn_asymp['oo'][0]}', lineStyle: Desmos.Styles.DASHED }});")
    if h_eqn_asymp['-oo'] != 'oo' and h_eqn_asymp['-oo'] != '-oo' and h_eqn_asymp['-oo'] != h_eqn_asymp['oo']:
        curves.append(f"calculator.setExpression({{ id: 'h_asymp_2', latex: 'y={h_eqn_asymp['-oo'][0]}', lineStyle: Desmos.Styles.DASHED }});")
    for x, y in h_eqn_asymp.items():
        eqn_limits.append(f'As x --> {x}, y --> {y[1]}.  ')
    eqn_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            curves.append(f"calculator.setExpression({{ id: 'v_asymp_{x}', latex: 'x={x}', lineStyle: Desmos.Styles.DASHED }});")
            eqn_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}.  ')
            eqn_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}.  ')
    else:
        eqn_limits.append('This equation has no vertical asymptotes')
    eqn_limits.append('<div class="space"></div>')

    h_eqn_asymp = der_asymptotes['h']
    v_eqn_asymp = der_asymptotes['v']
    for x, y in h_eqn_asymp.items():
        der_limits.append(f'As x --> {x}, y --> {y[1]}\n')
    der_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            der_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}')
            der_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}')
    else:
        der_limits.append('This equation\'s derivative has no vertical asymptotes')
    der_limits.append('<div class="space"></div>')

    h_eqn_asymp = double_der_asymptotes['h']
    v_eqn_asymp = double_der_asymptotes['v']
    for x, y in h_eqn_asymp.items():
        double_der_limits.append(f'As x --> {x}, y --> {y[1]}\n')
    double_der_limits.append('<div class="space"></div>')
    if type(v_eqn_asymp) is dict:
        for x, y in v_eqn_asymp.items():
            double_der_limits.append(f'As x --> {x} from the +ve, y --> {y["+"]}')
            double_der_limits.append(f'As x --> {x} from the -ve, y --> {y["-"]}')
    else:
        double_der_limits.append('This equation\'s double derivative has no vertical asymptotes')
    double_der_limits.append('<div class="space"></div>')


    curves_str = '\n		'.join(curves)
    html = html.replace("__EQUATIONS_HERE__", curves_str)
    eqn_limits_str = '\n	'.join(eqn_limits)
    der_limits_str = '\n	'.join(der_limits)
    double_der_limits_str = '\n	'.join(double_der_limits)
    html = html.replace("__EQN_LIMITS__", f'<h3>{eqn_limits_str}</h3>')
    html = html.replace("__DER_LIMITS__", f'<h3>{der_limits_str}</h3>')
    html = html.replace("__DOUBLE_DER_LIMITS__", f'<h3>{double_der_limits_str}</h3>')

    html = html.replace('XVALUES_HERE', x_values_table_str)
    html = html.replace('YVALUES_HERE', y_values_table_str)
    html = html.replace('DERIVATIVE_X_VALUES_HERE', der_xvals_table_str)
    html = html.replace('DERIVATIVE_Y_VALUES_HERE', der_yvals_table_str)
    html = html.replace('DOUBLE_DEV_X_VALUES_HERE', double_der_xvals_table_str)
    html = html.replace('DOUBLE_DEV_Y_VALUES_HERE', double_der_yvals_table_str)

    html = html.replace('__MAIN_EQUATION__', f'<h3>MAIN EQUATION: {eqn_str}</h3>')
    html = html.replace('__DERIVATIVE_EQN__', f'<h3>DERIVATIVE EQUATION: {eqn_formatter(eqn_formatter(desmos_der, maths=True), string=True, der=True)}</h3>')
    html = html.replace('__DOUBLE_DER_EQN__', f'<h3>DOUBLE DERIVATIVE EQUATION: {eqn_formatter(eqn_formatter(desmos_double_der, maths=True), string=True, double_der=True)}</h3>')

    filename = f'{int(time.time())}.html'
    outFile = open(filename, 'w')
    outFile.write(html)
    outFile.close()
    return filename


# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# TABLE BUILDER
# Creates a dictionary of x values with their associated y values
# Uses discontinuities to determine values of x values
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
def table_builder(discons, eqn, x):
    eqn_values = {}
    x_values = []
    y_values = []
    if discons:
        for value in discons:
            for i in range(-3, 4):
                a = value + i
                if a not in eqn_values.keys():
                    eqn_values[a] = 0
        for i in eqn_values.keys():
            if i in discons:
                eqn_values[i] = '*'
            else:
                eqn_values[i] = eqn.subs(x, i)
    else:
        for i in range(-3, 4):
            eqn_values[i] = eqn.subs(x, i)
    
    return eqn_values


# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# MATHS OPERATIONS
# Generates derivative and double derivative based on equation
# Creates tables of values for all equations
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
def maths_operations(eqn):
    x = Symbol('x', real=True)
    eqn = eval(eqn)
    try:
        eqn_discons = singularities(eqn, x)
    except:
        eqn_discons = []
    eqn_values = table_builder(eqn_discons, eqn, x)

    der = diff(eqn, x)
    try:
        der_discons = singularities(der, x)
    except:
        der_discons = []
    der_values = table_builder(der_discons, der, x)

    double_der = diff(eqn, x, x)
    try:
        double_der_discons = singularities(double_der, x)
    except:
        double_der_discons = []
    double_der_values = table_builder(double_der_discons, double_der, x)
    #for index, value in enumerate(y_values):
    #    y_values[index] = '%g'%(value) # remove trailing zeroes
    return eqn, eqn_values, der, der_values, double_der, double_der_values


# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# ASYMPTOTE CREATOR
# I hate asymptotes
# Calculates both horizontal and vertical asymptotes, as well as from which side they approach from
# asynced just in case calculating verticals takes too long, so i use wait_for with a 30 second timeout
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
async def asymptote_calculator(eqn):
    x = Symbol('x', real=True)
    h_asymptotes = {}

    pos_inf_h = limit(eqn, x, oo)
    try:
        if eqn.subs(x, 100) > pos_inf_h:
            pos_inf_h_str = f'{pos_inf_h} from the +ve'
        else:
            pos_inf_h_str = f'{pos_inf_h} from the -ve'
    except:
        pos_inf_h_str = str(pos_inf_h)

    neg_inf_h = limit(eqn, x, -oo)
    try:
        if eqn.subs(x, -100) > neg_inf_h:
            neg_inf_h_str = f'{neg_inf_h} from the +ve'
        else:
            neg_inf_h_str = f'{neg_inf_h} from the -ve'
    except:
        neg_inf_h_str = str(neg_inf_h)
    h_asymptotes['oo'] = [pos_inf_h, pos_inf_h_str]
    h_asymptotes['-oo'] = [neg_inf_h, neg_inf_h_str]

    n, d = fraction(simplify(eqn))
    denom_roots = solve(d)
    async def v_solver(eqn, x, denom_roots):
        v_asymptotes = {}
        if denom_roots:
            for root in denom_roots:
                v_asymptotes[root] = {}
                v_asymptotes[root]['+'] = limit(eqn, x, root)
                v_asymptotes[root]['-'] = limit(eqn, x, root, dir='-')
        return v_asymptotes

    if denom_roots:
        try:
            v_asymptotes = await asyncio.wait_for(v_solver(eqn, x, denom_roots), timeout=6)
        except:
            v_asymptotes = 'It took too long to calculate the vertical asymptotes give me a simpler equation smh'
        else:
            asymptotes = {}
            asymptotes['h'] = h_asymptotes
            asymptotes['v'] = v_asymptotes
    else:
        asymptotes = {}
        asymptotes['h'] = h_asymptotes
        asymptotes['v'] = 'That equation has no vertical asymptotes'

    return asymptotes


# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~
# GRAPH CREATOR
# The main function, this is where everything starts in the graphing process
# asynced because asymptote calculator requires an async function
# ~~~~~G~R~A~P~H~~~~C~O~D~E~~~~~~ 
async def graph_creator(eqn_str):
    maths_eqn = eqn_formatter(eqn_str, maths=True)

    eqn, eqn_values, der, der_values, double_der, double_der_values = maths_operations(maths_eqn)

    desmos_eqn = eqn_formatter(eqn_str, desmos=True)
    desmos_der = eqn_formatter(str(der), desmos=True)
    desmos_double_der = eqn_formatter(str(double_der), desmos=True)

    eqn_asymptotes = await asymptote_calculator(eqn)
    der_asymptotes = await asymptote_calculator(der)
    double_der_asymptotes = await asymptote_calculator(double_der)


    filename = desmos_html_creator(desmos_eqn, eqn_str, eqn_values, desmos_der, der_values, desmos_double_der, double_der_values, eqn_asymptotes, der_asymptotes, double_der_asymptotes)
    return filename




class Responses(Enum):
    SUCCESS     = 0
    RATE_LIMIT  = 1
    TWO_FACTOR  = 2
    BAD_CODE    = 3
    AUTH_FAIL   = 4


def val_details_fetcher() -> Dict:
    with open('txt_files/val_encrypted_details.txt', 'r') as inFile:
        val_details = json.loads(inFile.read())
    
    return val_details



def val_details_saver(val_details: Dict) -> None:
    with open('txt_files/val_encrypted_details.txt', 'w') as outFile:
        # print(val_details)
        outFile.write(json.dumps(val_details, indent=4))



def val_shop_fetcher() -> Dict:
    with open('txt_files/val_shop_details.txt', 'r') as inFile:
        val_shop = json.loads(inFile.read())
    
    return val_shop



def val_shop_saver(val_shop: Dict) -> None:
    with open('txt_files/val_shop_details.txt', 'w') as outFile:
        outFile.write(json.dumps(val_shop, indent=4))



def val_initial_check(uid: str) -> Any:
    val_shop = val_shop_fetcher()

    if val_shop[uid] == 0:
        return None
    
    expired = datetime.datetime.strptime(val_shop[uid]["expiry"], "%d/%m/%Y %H:%M:%S") - datetime.datetime.now()
    secs = expired.total_seconds()

    if secs <= 0:
        return None
    
    return val_shop[uid]



def val_credentials_storer(val_details: Dict, user_id: str, username: str, password: str) -> Dict:
    public, __ = rsa.newkeys(1024)
    with open('public.key', 'r') as inFile:
        public = rsa.PublicKey.load_pkcs1(inFile.read().encode('utf-8'))
    
    username_enc = rsa.encrypt(username.encode('utf-8'), public)
    password_enc = rsa.encrypt(password.encode('utf-8'), public)

    u_enc_b64 = base64.b64encode(username_enc).decode()
    p_enc_b64 = base64.b64encode(password_enc).decode()

    val_details[user_id] = [u_enc_b64, p_enc_b64]
    val_details_saver(val_details)

    return val_details



async def val_credentials_query(message: discord.Message) -> Tuple:
    author = message.author
    await author.create_dm()
    def check(m):
        return m.author == message.author

    await author.dm_channel.send("i need your riot username and password (don't worry all data is encrypted)\nfirst, send through your username")
    try:
        msg = await client.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await author.dm_channel.send("timed out, start again")
        return None, None
    
    username = msg.content

    await author.dm_channel.send("ok now your password")
    try:
        msg = await client.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await author.dm_channel.send("timed out, start again")
        return None, None
    
    password = msg.content

    return (username, password)


async def val_credentials_getter(message: discord.Message, force=False, uid=None):
    if uid is None:
        user_id = str(message.author.id)
    else:
        user_id = uid

    val_details = val_details_fetcher()

    if val_details[user_id] == 0 or force:
        username, password = await val_credentials_query(message)
        
        if username is None:
            return None, None

        val_credentials_storer(val_details, user_id, username, password)
    else:
        with open('private.key', 'r') as inFile:
            private = rsa.PrivateKey.load_pkcs1(inFile.read().encode('utf-8'))
        details = val_details.get(user_id)
        u_enc = base64.b64decode(details[0].encode())
        p_enc = base64.b64decode(details[1].encode())
        username = rsa.decrypt(u_enc, private).decode()
        password = rsa.decrypt(p_enc, private).decode()

    return username, password



def lunac_store_get(username: str, password: str, region: str = "AP") -> Tuple:
    print(region)
    u_b64 = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    p_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    headers = {
        'Origin': 'https://valorantstore.net',
        'Referer': 'https://valorantstore.net/'
    }

    r = requests.get(
        f'https://api.lunac.xyz/valorant/getPlayerStoreFront/{u_b64}/{region}/{p_b64}',
        headers = headers
    )

    print(r)
    print(r.headers)
    response = r.json()
    print(response)
    error = response.get("Error")

    if error is None:
        return (Responses.SUCCESS, response)
    elif error == "2fa":
        return (Responses.TWO_FACTOR, u_b64)
    elif "limit" in error.lower():
        # print(error)
        return (Responses.RATE_LIMIT, None)
    else:
        print(error)
        return (Responses.AUTH_FAIL, None)



def lunac_store_2fa(u_b64: str, code: str):

    r = requests.get(
        f'https://api.lunac.xyz/valorant/getPlayerStoreFront2fa/{code}/{u_b64}',
    )

    response = r.json()
    error = response.get("Error")

    if error is None:
        return (Responses.SUCCESS, response)
    else:
        return (Responses.BAD_CODE, None)



async def get_2fa(author) -> str:
    await author.create_dm()
    def check(m):
        return m.author == author

    await author.dm_channel.send("send through the 2FA code that was sent to your email")

    try:
        msg = await client.wait_for('message', timeout=90.0, check=check)
    except asyncio.TimeoutError:
        await author.dm_channel.send("timed out, start again")
        return None

    return msg.content



async def get_region(author) -> str:
    await author.create_dm()
    def check(m):
        return m.author == author

    await author.dm_channel.send("send through the specified region for your account (AP, EU or US)")

    try:
        msg = await client.wait_for('message', timeout=90.0, check=check)
    except asyncio.TimeoutError:
        await author.dm_channel.send("timed out, start again")
        return None

    return msg.content



async def lunac_store(username: str, password: str, author, region: bool = False):
    if region:
        reg = await get_region(author)
        reg = reg.upper()
    else:
        reg = "AP"

    response = lunac_store_get(username, password, reg)
    err = response[0]
    
    if err == Responses.RATE_LIMIT or err == Responses.AUTH_FAIL:
        return err

    elif err == Responses.SUCCESS:
        return response[1]

    # 2FA is enabled, get code
    code = await get_2fa(author)
    if code is None:
        return None
    
    response = lunac_store_2fa(response[1], code)
    err = response[0]

    if err == Responses.BAD_CODE:
        return err
    
    return response[1]



async def rate_limit_msg(author):
    await author.create_dm()
    await author.dm_channel.send("too many requests, slow down")



async def auth_fail_msg(author):
    await author.create_dm()
    await author.dm_channel.send("authentication failed for some reason, try re-entering your login by typing \"valorant store login\"")



async def bad_code_msg(author):
    await author.create_dm()
    await author.dm_channel.send("invalid 2FA code, try again from the beginnging")



def store_offer_getter() -> Any:
    r = requests.get("https://api.henrikdev.xyz/valorant/v1/store-offers")
    return r.json().get("data").get("Offers")



def skins_info_getter() -> Any:
    r = requests.get("https://valorant-api.com/v1/weapons/skins")
    return r.json().get("data")



def store_response_parse(username: str, response: Any) -> List:
    item_info = {
        "username":     username,
        "expiry":       None,
        "index":        0,
        "lvlIndex":     0,
        "chromaIndex":  0,
        "data":         []
    }
    item_ids = response.get("SkinsPanelLayout").get("SingleItemOffers")
    store_offers = store_offer_getter()
    skin_info = skins_info_getter()
    relevant_offers = []
    relevant_skins = []

    for offer in store_offers:
        if offer.get("OfferID") in item_ids:
            relevant_offers.append(offer)
    
    for skin in skin_info:
        if skin.get("levels")[0].get("uuid") in item_ids:
            relevant_skins.append(skin)
    
    relevant_offers.sort(key = lambda x: x.get("OfferID"))
    relevant_skins.sort(key = lambda x: x.get("levels")[0].get("uuid"))

    timeRemaining = response.get("SkinsPanelLayout").get("SingleItemOffersRemainingDurationInSeconds")
    expiryDate = datetime.datetime.now() + datetime.timedelta(seconds = timeRemaining)
    expiryStr = expiryDate.strftime("%d/%m/%Y %H:%M:%S")
    item_info["expiry"] = expiryStr

    for i in range(len(relevant_offers)):
        name = relevant_skins[i].get("displayName")
        icon = relevant_skins[i].get("chromas")[0].get("displayIcon")
        if icon is None:
            icon = relevant_skins[i].get("displayIcon")
        if icon is None:
            icon = relevant_skins[i].get("levels")[0].get("displayIcon")
        if icon is None:
            icon = f"https://media.valorant-api.com/weaponskinlevels/{relevant_skins[i]['levels'][0]['uuid']}"

        item_info["data"].append({
            "name":             name,
            "cost":             list(relevant_offers[i].get("Cost").values())[0],
            "icon":             icon,
            "video":            relevant_skins[i].get("streamedVideo"),
            "chromas":          [],
            "levels":           []
        })

        chromas = relevant_skins[i].get("chromas")
        levels = relevant_skins[i].get("levels")

        if len(chromas) > 1:
            for j in range(1, len(chromas)):
                item_info["data"][i]["chromas"].append({
                    "name":     chromas[j].get("displayName").split(f"{name} ")[1],
                    "icon":     chromas[j].get("displayIcon"),
                    "video":    chromas[j].get("streamedVideo")
                })
        
        if len(levels) > 1:
            for j in range(1, len(levels)):
                try:
                    t = levels[j].get("levelItem").split("::")[1]
                except (AttributeError, IndexError):
                    t = None
                
                item_info["data"][i]["levels"].append({
                    "name":     levels[j].get("displayName").split(f"{name} ")[1],
                    "type":     t,
                    "icon":     levels[j].get("displayIcon"),
                    "video":    levels[j].get("streamedVideo")
                })
    
    return item_info



def auth_riotgames_login(username: str, password: str, region):
    s = requests.session()

    data = {
        "client_id": "play-valorant-web-prod",
        "nonce": "1",
        "redirect_uri": "https://playvalorant.com/opt_in",
        "response_type": "token id_token"
    }
    s.post("https://auth.riotgames.com/api/v1/authorization", json=data)

    data = {
        "type": "auth",
        "username": f"{username}",
        "password":  f"{password}"
    }
    r = s.put("https://auth.riotgames.com/api/v1/authorization", json=data)
    pattern = regex.compile(r"access_token=([a-zA-Z\d\.\-\_)]*)")
    access_token = pattern.findall(r.json()["response"]["parameters"]["uri"])[0]

    data = {}
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    r = s.post("https://entitlements.auth.riotgames.com/api/token/v1", json=data, headers=headers)
    entitlements_token = r.json()["entitlements_token"]

    r = s.post("https://auth.riotgames.com/userinfo", headers=headers)
    user_id = r.json()["sub"]

    headers["X-Riot-Entitlements-JWT"] = entitlements_token
    response = s.get(f"https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}")

    return response.json()



async def official_val_store(username: str, password: str, author, region: bool = False):
    if region:
        reg = await get_region(author)
        reg = reg.lower()
    else:
        reg = "ap"

    response = auth_riotgames_login(username, password, reg)
    




async def store_fetcher(message: discord.Message, refresh: bool = False, region: bool = False, lunac=True):
    if refresh is False:
        item_info = val_initial_check(str(message.author.id))
        if item_info is not None:
            return item_info
    
    username, password = await val_credentials_getter(message)
    if username is None:
        return None
    
    if lunac:
        response = await lunac_store(username, password, message.author, region)
        if response is None:
            return None
        elif response == Responses.RATE_LIMIT:
            await rate_limit_msg(message.author)
            return None
        elif response == Responses.AUTH_FAIL:
            await auth_fail_msg(message.author)
            return None
        elif response == Responses.BAD_CODE:
            await bad_code_msg(message.author)
            return None
    
    else:
        response = await official_val_store(username, password, message.author, region)
    
    item_info = store_response_parse(username, response)
    val_shop = val_shop_fetcher()
    val_shop[str(message.author.id)] = item_info
    val_shop_saver(val_shop)

    return item_info

    

def val_embed_generator(item_info: dict, store: bool = True, levels: bool = True) -> discord.Embed:
    current = item_info["data"][item_info["index"]]
    
    if store:
        embed = discord.Embed(
            title = f"{item_info['username']}'s Store",
            type = "rich",
            description = f"The daily store page for {item_info['username']}.\n"\
                "⏪ ⏩ = Page Turn\n"\
                "ℹ️ = Info about current skin (if applicable)",
            colour=discord.Colour(0xfa4454)
        )
        embed.set_image(url=current["icon"])
        embed.add_field(name="Name", value=current["name"], inline=True)

    elif levels:
        lvl = current['levels'][item_info['lvlIndex']]
        name = current['name']

        embed = discord.Embed(
            title = f"{name} Level Data",
            type = "rich",
            description = f"Level info for {name}\n"\
                "⏪ ⏩ = Page Turn\n"\
                "🎨 = Switch to Chromas (Skin Colour Variations)\n"\
                "↩️ = Back to store",
            colour=discord.Colour(0xfa4454)
        )
        embed.set_image(url=(lvl['icon'] if lvl['icon'] is not None else current['icon']))
        embed.add_field(name="Level", value=lvl["name"], inline=True)

        if lvl["type"] is not None:
            embed.add_field(name="Type", value=lvl["type"], inline=True)
        if lvl["video"] is not None:
            embed.add_field(name="Video", value=lvl["video"], inline=False)

    else:
        chroma = current['chromas'][item_info['chromaIndex']]
        name = current['name']

        embed = discord.Embed(
            title = f"{name} Chroma Data",
            type = "rich",
            description = f"Chroma info for {name}\n"\
                "⏪ ⏩ = Page Turn\n"\
                "⬆️ = Switch to Levels (Skin Additions)\n"\
                "↩️ = Back to store",
            colour=discord.Colour(0xfa4454)
        )
        embed.set_image(url=(chroma['icon'] if chroma['icon'] is not None else current['icon']))
        embed.add_field(name="Level", value=chroma["name"], inline=True)

        if chroma["video"] is not None:
            embed.add_field(name="Video", value=chroma["video"], inline=False)

    embed.add_field(name="Cost", value=f'{current["cost"]} VP', inline=True)
    embed.add_field(name="Expiry", value=item_info["expiry"], inline=True)
    return embed



def val_reaction_list_gen(item_info: dict, store: bool = True, levels: bool = True) -> List:
    reaction_list = []

    if store:
        index = item_info["index"]

        if index == 0:
            reaction_list.insert(0, '⏩')
        elif index == (len(item_info["data"]) - 1):
            reaction_list.insert(0, '⏪')
        else:
            reaction_list.insert(0, '⏪')
            reaction_list.insert(1, '⏩')

        if (item_info["data"][item_info["index"]]["chromas"] != []) and \
            (item_info["data"][item_info["index"]]["levels"] != []):
            reaction_list.append('ℹ️')
            
    elif levels:
        index = item_info["lvlIndex"]

        if index == 0:
            reaction_list.insert(0, '⏩')
        elif index == (len(item_info["data"][item_info["index"]]["levels"]) - 1):
            reaction_list.insert(0, '⏪')
        else:
            reaction_list.insert(0, '⏪')
            reaction_list.insert(1, '⏩')

        if item_info["data"][item_info["index"]]["chromas"] != []:
            reaction_list.append('🎨')
        reaction_list.append('↩️')

    else:
        index = item_info["chromaIndex"]
        
        if index == 0:
            reaction_list.insert(0, '⏩')
        elif index == (len(item_info["data"][item_info["index"]]["chromas"]) - 1):
            reaction_list.insert(0, '⏪')
        else:
            reaction_list.insert(0, '⏪')
            reaction_list.insert(1, '⏩')
        
        if item_info["data"][item_info["index"]]["levels"] != []:
            reaction_list.append('⬆️')
        reaction_list.append('↩️')

    return reaction_list



async def valorant_message_creator(item_info: dict, channel, msg: discord.Message, store: bool = True, levels: bool = True):
    embed = val_embed_generator(item_info, store=store, levels=levels)
    reaction_list = val_reaction_list_gen(item_info, store=store, levels=levels)

    if msg is None:
        msg = await channel.send(embed=embed)
    else:
        if channel.type == discord.ChannelType.private:
            await msg.delete()
            msg = await channel.send(embed=embed)
        else:
            await msg.clear_reactions()
            await msg.edit(embed=embed)
    
    for emoji in reaction_list:
        await msg.add_reaction(emoji)

    def check(reaction, user):
        return user != client.user and str(reaction.emoji) in reaction_list and reaction.message.id == msg.id
    
    try:
        reaction, __ = await client.wait_for('reaction_add', timeout=120.0, check=check)
    except asyncio.TimeoutError:
        return None, None, None, None
    else:
        react = str(reaction.emoji)

        if store:
            if react == '⏩':
                item_info["index"] += 1
            # item_info["lvlIndex"] += 1
            # item_info["chromaIndex"] += 1
            elif react == '⏪':
                item_info["index"] -= 1
            # item_info["lvlIndex"] -= 1
            # item_info["chromaIndex"] -= 1
            elif react == 'ℹ️':
                store = False
                levels = True

        elif levels:
            if react == '⏩':
                item_info["lvlIndex"] += 1
            elif react == '⏪':
                item_info["lvlIndex"] -= 1
            elif react == '↩️':
                store = True
                levels = True
            elif react == '🎨':
                levels = False
        
        else:
            if react == '⏩':
                item_info["chromaIndex"] += 1
            elif react == '⏪':
                item_info["chromaIndex"] -= 1
            elif react == '↩️':
                store = True
                levels = True
            elif react == '⬆️':
                levels = True

        return item_info, store, levels, msg



async def valorant_message_handler(item_info: dict, message: discord.Message):
    store = True
    levels = True
    msg = None
    item_info["index"] = 0
    item_info["lvlIndex"] = 0
    item_info["chromaIndex"] = 0

    while True:
        item_info, store, levels, msg = await valorant_message_creator(item_info, message.channel, msg, store, levels)
        
        if item_info is None:
            break



async def valorant_store_checker(message: discord.Message, refresh: bool = False, region: bool = False):
    item_info = await store_fetcher(message, refresh, region)

    if item_info is None:
        return None

    await valorant_message_handler(item_info, message)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ON MESSAGE (i.e. THE BIG BOY)
# all previous functions are mere foreplay, nothing to the scale of this hefty function
# except for other client events, THIS IS WHERE EVERYTHING HAPPENS
# List of current functions:
    # Audio file/command manager
    # Grant insult interpreter
    # Swear parser
    # Emoji-block-letters message converter
    # kpop
        # message checker
        # history checker
        # current username/nickname checker (nickname function obsolete due to on_member_update)
        # optical recognition checker (allows barney to scan images for 'kpop')
        # coupon creator and reader via qr code
    # Schoology assignment displayer
    # delivery persion identifier (checks for 'feedback')
    # Schmalex + schmalvin parser
    # Classroom voice channel manager
    # The entire fucking mafia script which, in hindsight, probs should be its own function and not all nested within on_message, but eh
    # General fuckery parser
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_message(message):
    #global previous_5_messages
    if message.channel.id == 473065916100378624: # archive 2
        return
    elif message.channel.id == 210716706501296128: # archive 1
        return
    elif message.channel.id == 704223849939599370: # bot discuss ryan's server
        return
    if message.author == client.user or message.author.id == 247852652019318795 or message.author.id == 732621248395346020: # dad and zinger bot
        return

    msg = message.content.lower()
    triggered = False
    kpop_detection = False

    global kpop_pattern
    global swear_pattern
    global bazinga
    global unicode_dict
    global emoji_regex
    global whos_listening_to_who
    

    # async for sent_message in message.channel.history(limit=1):
    #     if sent_message.author == client.user and sent_message.content == 'what do you want to send':
    #         return

    if kpop_detection:
# ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
# KPOP MESSAGE ID OPENER
# Reads from the saved list of kpop message IDs, required for the history check to work properly and not repeatedly ban people
# TODO:
    # convert kpop_message_id_list into a dictionary for the id of each channel, so that size of the file can be limited i.e. max 20 for each channel
        # do dm_channels get a new ID everytime they are created? if so, then dm_channels will all have to fall under on big dictionary key
    # Add a kpop_message_id_list size limiter
# ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        inFile = open('txt_files/kpop_message_id_list.txt')
        kpop_message_id_list = json.loads(inFile.read())
        inFile.close()

    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
    # KPOP IMMUNITY CHECKER
    # Checks to see if a user has kpop immunity from a coupon
    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        immune = False
        kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
        if str(message.author.id) in kpop_coupons_users.keys():
            if kpop_coupons_users[str(message.author.id)] >= int(time.time()):
                immune = True
            elif kpop_coupons_users[str(message.author.id)] < int(time.time()):
                del kpop_coupons_users[str(message.author.id)]
                outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                outFile.write(json.dumps(kpop_coupons_users))
                outFile.close()



    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
    # KPOP MESSAGE CHECKER
    # Basic kpop_pattern regex check within a user's message
    # If successful, message is appended to the kpop_message_list and runs the kpop_kicker
    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        
        if kpop_pattern.search(message.system_content.lower().replace(u'\xa0', u' ')):
            kpop_message_id_list.append(message.id)
            outFile = open('txt_files/kpop_message_id_list.txt', 'w')
            outFile.write(json.dumps(kpop_message_id_list))
            outFile.close()
            if not immune:
                await kpop_kicker(message.channel, message.author)
                return None

    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
    # KPOP MESSAGE HISTORY CHECKER
    # Checks channel history to see if any sneaky bastards edited their previous messages to say a message that would otherwise be detected by kpop_pattern regex 
    # Reads kpop_message_list to see if this message had been identified before
    # If not, appends if it to kpop_message_list and runs the kpop_kicker
    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        else:
            kicked = False
            async for sent_message in message.channel.history(limit=20):
                #print(sent_message.system_content)
                if (kpop_pattern.search(sent_message.system_content.lower().replace(u'\xa0', u' '))) and (sent_message.id not in kpop_message_id_list) and (sent_message.author != client.user):
                    
                    kpop_coupons_users = json.loads(open('txt_files/kpop_coupons_users.txt').read())
                    if str(sent_message.author.id) in kpop_coupons_users.keys():
                        if kpop_coupons_users[str(sent_message.author.id)] >= int(time.time()):
                            immune = True
                        elif kpop_coupons_users[str(sent_message.author.id)] < int(time.time()):
                            del kpop_coupons_users[str(sent_message.author.id)]
                            outFile = open('txt_files/kpop_coupons_users.txt', 'w')
                            outFile.write(json.dumps(kpop_coupons_users))
                            outFile.close()

                    kicked = True
                    kpop_message_id_list.append(sent_message.id)
                    outFile = open('txt_files/kpop_message_id_list.txt', 'w')
                    outFile.write(json.dumps(kpop_message_id_list))
                    outFile.close()
                    if not immune:
                        await sent_message.channel.send(f'did you really think i can\'t read edited messages {sent_message.author.mention}? don\'t say the k word again.')
                        await kpop_kicker(sent_message.channel, sent_message.author)

            if not kicked:
                if not immune:
                    await backup_kpop_check(message.system_content, message.author, message.guild, nick=False, message=message)




    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
    # KPOP USERNAME AND NICKNAME CODE
    # checks message author's username and nickname for kpop_pattern regex
    # nickname is semi-obsolete, as this is now managed by on_member_update
    # but this is still used if nickname is changed during barney down time
    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        if not immune:
            try:
                name = message.author.nick.replace(u'\xa0', u' ')
            except:
                name = message.author.name.replace(u'\xa0', u' ')
            if not name:
                name = message.author.name.replace(u'\xa0', u' ')
            if kpop_pattern.search(name):
                await message.channel.send('i can read your name')
                await kpop_kicker(message.channel, message.author)
            else:
                await backup_kpop_check(name, message.author, message.guild, nick=True)



    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
    # KPOP OCR DETECTION + KPOP COUPON DETECTION
    # Uses tesseract-ocr with pytesseract to search images for text that would otherwise trigger the kpop_pattern regex
    # Before downloading attachments, checks to see if it's an image
    # locally stored using requests instead of await attachment.save like in the audio code
    # Also checks for kpop coupon code 
    # ~~~~~~~~~~~K~~P~~O~~P~~~~~~~~~~
        if len(message.attachments) > 0:
            kicked = False
            for attachment in message.attachments:
                if '.jpg' not in message.attachments[0].filename and '.png' not in message.attachments[0].filename and '.jpeg' not in message.attachments[0].filename:
                    continue
                else:
                    print('hi you said the word kpop')
                    response = requests.get(attachment.url)
                    img = Image.open(io.BytesIO(response.content))
                    text = pytesseract.image_to_string(img)
                    if kpop_pattern.search(text):
                        if not immune:
                            if not kicked:
                                await message.channel.send('i can read images...')
                                kicked = True
                                await kpop_kicker(message.channel, message.author)
                                return None           
                    elif img.size == (1152, 648):
                        response = kpop_coupon_redeemer(img, message.author)
                        if response:
                            await message.channel.send(response)
                            return None
                    else:
                        await backup_kpop_check(text, message.author, message.guild, custom_response='i can read images...')

        if message.embeds:
            # print(message.embeds)
            for embed in message.embeds:
                try:
                    response = requests.get(embed.url)
                    img = Image.open(io.BytesIO(response.content))
                    text = pytesseract.image_to_string(img)
                    if kpop_pattern.search(text):
                        # print(text)
                        if not immune:
                            if not kicked:
                                await message.channel.send('i can read images...')
                                kicked = True
                                await kpop_kicker(message.channel, message.author)
                                return None           
                    elif img.size == (1152, 648):
                        response = kpop_coupon_redeemer(img, message.author)
                        if response:
                            await message.channel.send(response)
                            return None
                    else:
                        await backup_kpop_check(text, message.author, message.guild, custom_response='i can read images...')
                except:
                    continue



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# KPOP COUPON CREATOR
# creates a kpop coupon
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if 'qr code' == msg and message.author.id == 203672102509740042:
        await message.channel.send('choose between "24_hours", "3_days", "7_days"')
        def check(m):
            return m.author == message.author and (m.content.lower() == '24_hours' or m.content.lower() == '3_days' or m.content.lower() == '7_days')
        try:
            template = await client.wait_for('message', timeout=20.0, check=check)
        except:
            await message.author.dm_channel.send('ok fine dont send anything')
            return None
        else:
            await message.author.dm_channel.send(f'ok making a {template.content} qr code')
        await message.author.dm_channel.send(kpop_qr_creator(template.content))
        return None





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUDIO COMMAND VOICE JOINER
# checks if message contained a voice command, following by a check that the user is in a voice channel
# if successful, runs voice_joiner function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    inFile = open("txt_files/audio_command_linker.txt")
    x = inFile.read()
    audio_command_file = json.loads(x)
    inFile.close()
    if msg in audio_command_file.keys():
        try:
            channel = message.author.voice.channel
        except:
            channel = None
        if not channel:
            await message.channel.send('you must be in a voice channel to get me to play a file')
            return None
        else:
            file_names = audio_command_file[msg]
            file_names_list = list(file_names.keys())
            await voice_joiner(message, client, file_names_list)
            return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# AUDIO FILE SAVER
# Manages the saving of audio files, as well as the creation of their command associations
# 1mb size limit, checks for duplicate files, checks for .mp3
# If duplicate command is provided, then file is added to that command association, and the file that is to be played will be randomly chosen when command is called
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    if msg[:15] == "save audio file":
        if len(message.attachments) > 1:
            await message.channel.send("too many attachments, attach files one at a time")
            return None
        elif len(message.attachments) == 0:
            await message.channel.send("i mean like you gotta attach an mp3 file for me to save, i'm not a wizard i can't just reach into ur computer and choose a file")
            return None
        else:
            attachment = message.attachments[0]
            if attachment.size > 1100000:
                await message.channel.send("file too big, make it less than a mb")
                return None
            else:
                if ".mp3" != attachment.filename[-4:]:
                    await message.channel.send("only send me .mp3 files")
                    return None
                else:
                    inFile = open("txt_files/audio_file_list.txt")
                    x = inFile.read()
                    audio_names_dict = json.loads(x)
                    inFile.close()
                    if attachment.filename in audio_names_dict.keys():
                        await message.channel.send("i've already got a file of that name. call it something else and try again.")
                        return None
                    else:
                        try:
                            command_list = regex.findall(r'\"(.*?)\"', message.system_content.lower())
                            print(command_list)
                            if not command_list:
                                await message.channel.send("something went wrong identifying your command(s). make sure you use \"double quotes\" around each phrase you want to be able to trigger your file")
                                return None
                            else:
                                await attachment.save(f'audio_files/{attachment.filename}')
                                audio_names_dict[attachment.filename] = message.author.id
                                outFile = open('txt_files/audio_file_list.txt', 'w')
                                outFile.write(json.dumps(audio_names_dict))
                                outFile.close()
                                inFile = open('txt_files/audio_command_linker.txt')
                                x = inFile.read()
                                audio_command_dict = json.loads(x)
                                inFile.close()
                                for command in command_list:
                                    try:
                                        audio_command_dict[command][attachment.filename] = message.author.id
                                    except:
                                        command_file_dict = {attachment.filename: message.author.id}
                                        audio_command_dict[command] = command_file_dict
                                print(audio_command_dict)
                                command_list_str = '\n'.join(command_list)
                                await message.channel.send(f"your file, {attachment.filename} has been saved, and can be said by the following triggers:\n{command_list_str}")
                                outFile = open('txt_files/audio_command_linker.txt', 'w')
                                outFile.write(json.dumps(audio_command_dict))
                                outFile.close()
                                return None
                        except:
                            await message.channel.send("something went wrong identifying your command(s). make sure you use \"double quotes\" around each phrase you want to be able to trigger your file")
                            return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# AUDIO COMMAND DELETER
# Manages the deletion of audio commands
# Only allows deletion if user requests a command they created
# If command contains multiple file associations, then those file command associations
# If a file, after command deletion, has no associations, the file is then subsequently deleted, and the user is notified
# Due to the code logic, this will always be a file that the user owns, so no permission conflicts are created
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif msg[:20] == 'delete audio command':
        inFile = open('txt_files/audio_command_linker.txt')
        x = inFile.read()
        audio_command_dict = json.loads(x)
        inFile.close()
        m = regex.search(r'\"(.*?)\"', message.system_content.lower())
        try:
            command = m.group(1)
            user_id = message.author.id
            if command not in audio_command_dict.keys():
                await message.channel.send("that command doesn't exist")
                return None
            command_files = audio_command_dict[command]
            file_name_list = []
            kept_file_dict = {}
            for file_name in list(command_files.keys()):
                if command_files[file_name] == message.author.id or message.author.id == 203672102509740042: #i have override
                    file_name_list.append(file_name)
                    del command_files[file_name]
                else:
                    kept_file_dict[file_name] = command_files[file_name]
            
            response = f"ok, so i tried to removed following file associations that you added with \"{command}\": {', '.join(file_name_list)}."
            #print(f"\n\nAUDIO COMMAND DICT\n{audio_command_dict}\n\n")
            if len(kept_file_dict.keys()) == 0:
                #print(f"\n\nAUDIO COMMAND DICT\n{audio_command_dict}\n\n")
                del audio_command_dict[command]
                #print(f"\n\nAUDIO COMMAND DICT\n{audio_command_dict}\n\n")
                response += f"\nsince you were the only one that had any files linked to \"{command}\", i deleted the command."
            elif len(kept_file_dict.keys()) > 0:
                owner_mention_dict = {}
                for audio_file in list(kept_file_dict.keys()):
                    owner_id = kept_file_dict[audio_file]
                    owner = client.get_user(owner_id)
                    owner_mention_dict[owner_id] = owner.mention
                #print(f"\n\nAUDIO COMMAND DICT\n{audio_command_dict}\n\n")
                file_mention_string = ''
                for x in kept_file_dict.keys():
                    file_mention_string += f"{owner_mention_dict[kept_file_dict[x]]}: {x}"
                response += f"\ni tried to delete \"{command}\", but you didn't upload all the files linked to that command, so i didn't. ask these people about these files: {file_mention_string}"
            repeat_dict = {}
            for command in list(audio_command_dict.keys()):
                audio_file_dict = audio_command_dict[command]
                for audio_file in list(audio_file_dict.keys()):
                    for file_name in file_name_list:
                        if audio_file == file_name:
                            repeat_dict[file_name] = True
            deleted_file_list = []
            #print(f"\n\nREPEAT DICT\n{repeat_dict}\n\n")
            for file_name in list(repeat_dict.keys()):
                if repeat_dict[file_name]:
                    file_name_list.remove(file_name)
            #print(f"\n\nFILE NAME LIST\n{file_name_list}\n\n")
            if len(file_name_list) > 0:
                for command in list(audio_command_dict.keys()):
                    for x in file_name_list:
                        try:
                            del audio_command_dict[command][x]
                        except:
                            continue
                for x in file_name_list:
                    os.remove(f'audio_files/{x}')
                response += f"\nsince there were no other commands used to trigger: {', '.join(file_name_list)}, i removed those files."
            inFile = open("txt_files/audio_file_list.txt")
            x = inFile.read()
            audio_file_dict = json.loads(x)
            inFile.close()
            for x in file_name_list:
                del audio_file_dict[x]
            outFile = open("txt_files/audio_file_list.txt", "w")
            x = json.dumps(audio_file_dict)
            outFile.write(x)
            outFile.close()
            outFile = open("txt_files/audio_command_linker.txt", "w")
            #print(f"\n\nAUDIO COMMAND DICT\n{audio_command_dict}\n\n")
            x = json.dumps(audio_command_dict)
            #print(f"\n\n{x}\n\n")
            outFile.write(x)
            outFile.close()
            #print(f"\n\n{file_name_list}\n\n")
                
            
            await message.channel.send(response)
            return None


        except AttributeError:
            await message.channel.send("that is not a valid command name. make sure you use \"double quotes\" around the command you want to remove.") 
            return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUDIO FILE DELETER
# Manages the deletion of audio files
# Only allows the user to delete an audio file they created
# If, after file deletion, an empty trigger command exists, it is deleted and the user is subsequently notified
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif msg[:17] == "delete audio file":
        inFile = open('txt_files/audio_file_list.txt')
        x = inFile.read()
        audio_file_dict = json.loads(x)
        inFile.close()
        m = regex.search(r'\"(.*?)\"', message.system_content.lower())
        try:
            file_to_delete = m.group(1)
            user_id = message.author.id
            if file_to_delete not in audio_file_dict.keys():
                await message.channel.send("that file doesn't exist")
                return None
            if audio_file_dict[file_to_delete] != user_id and user_id != 203672102509740042: # i have manual override
                await message.channel.send("you didn't upload that file, so you cannot remove it.")
                return None
            del audio_file_dict[file_to_delete]
            outFile = open('txt_files/audio_file_list.txt', "w")
            x = json.dumps(audio_file_dict)
            outFile.write(x)
            outFile.close()
            inFile = open('txt_files/audio_command_linker.txt')
            x = inFile.read()
            audio_command_dict = json.loads(x)
            inFile.close()
            deleted_commands = []
            for command in list(audio_command_dict.keys()):
                temp_dict = audio_command_dict[command]
                for file_name in list(temp_dict.keys()):
                    if file_name == file_to_delete:
                        del audio_command_dict[command][file_name]
                        if not audio_command_dict[command]:
                            del audio_command_dict[command]
                            deleted_commands.append(command)
            outFile = open('txt_files/audio_command_linker.txt', "w")
            x = json.dumps(audio_command_dict)
            outFile.write(x)
            outFile.close()
            os.remove(f'audio_files/{file_to_delete}')
            if deleted_commands:
                deleted_command_str = f"\ni deleted the following commands: {', '.join(deleted_commands)}, as they only linked to the file you just deleted."
            else:
                deleted_command_str = ''
            response = f"i removed your file, {file_to_delete}.{deleted_command_str}"

            await message.channel.send(response)
            return None

        except AttributeError:
            await message.channel.send("that is not a valid audio file name. make sure you use \"double quotes\" around the command you want to remove.")
            return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DISPLAY AUDIO COMMANDS
# Sends a direct message to the user with all current audio file command associations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif "display audio commands" == msg:
        final_str = ''
        for command in audio_command_file.keys():
            final_str += f"{command}: "
            file_name_list = list(audio_command_file[command].keys())
            final_str += ', '.join(file_name_list)
            final_str += '\n'
        final_str_list = list(final_str)
        new_final_str_list = []
        for char in final_str_list:
            if char == "*" or char == "_":
                new_final_str_list.append(f'\\{char}')
                continue
            else:
                new_final_str_list.append(char)
        final_str = ''.join(new_final_str_list)
        inFile = open('txt_files/audio_file_list.txt')
        x = inFile.read()
        audio_file_dict = json.loads(x)
        inFile.close()
        user_str = ''
        for file_name in audio_file_dict.keys():
            user_id = audio_file_dict[file_name]
            owner = client.get_user(user_id)
            user_str += f"\n{file_name}: {owner.mention}"
        user_str_list = list(user_str)
        new_user_str_list = []
        for char in user_str_list:
            if char == "*" or char == "_":
                new_user_str_list.append(f'\\{char}')
                continue
            else:
                new_user_str_list.append(char)
        user_str = ''.join(new_user_str_list)
        await message.channel.send("a list has been dmed to you")
        await message.author.create_dm()
        await message.author.dm_channel.send(f"here are all my commands, and the files they may trigger:\n{final_str}.\nthe files were uploaded by these people: {user_str}")
        return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUDIO HELP
# Sends a help message to the message's channel outlining all of barney's audio functions and how to use them
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif "audio help" == msg:
        await message.channel.send("use \'save audio file \"<trigger word>\" \"<trigger word2>\"\' etc. to create a file assocation. make sure to use double quotes, and ensure the file you uploaded is a .mp3, 1mb limit\nuse \'delete audio command \"<command>\"\' to delete a specific command. this will only delete file associations for files you uploaded. if you uploaded all the files for that trigger word, the command will be deleted.\nuse \'delete audio file \"<file.mp3>\"\' to delete a file you uploaded. this will delete a trigger word if it was only being used for that file.\nuse \'display audio commands\' to get a list of all current associations dmed to you.")
        return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VOICE RECOGNITION INITIALISER
# Allows the voice recog handler to listen to up to 3 users at any time
# This might be slightly memory intensive idk we'll see
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if message.content[:10] == 'listen to ':
        triggered = True
        user = None
        name_to_check = message.content[10:]
        user = message.guild.get_member_named(name_to_check)
        if not user:
            await message.channel.send(f'unable to find user {name_to_check}')
        elif not user.voice.channel:
            await message.channel.send(f'{user.name} is not in a voice channel')
        elif message.author.id in whos_listening_to_who.keys():
            await message.channel.send('you\'ve already requested to listen to someone')
        else:
            voice_id = message.guild.get_channel(user.voice.channel.id)
            if not voice_id:
                await message.channel.send('can\'t listen to that user, they may be in a vc in a different server')
            else:
                await voice_receive_controller(user.id, user.voice.channel.id, message)
    

    elif msg == 'stop listening':
        triggered = True
        filename = await voice_receive_leave(message)
        if filename:
            try:
                transcript = discord.File(filename)
                await message.channel.send('here\'s your transcript', file=transcript)
                os.remove(filename)
            except Exception as e:
                print(e)
                await message.channel.send('couldn\'t get your transcript soz lol')

        
    if msg == 'member list' and message.author.id == 203672102509740042:
        name_list,id_list,x=[],[],''
        for member in message.guild.members:
            name_list.append(member.name)
            id_list.append(member.id)
        for i in range(0, len(name_list)):
            x = x + f'{name_list[i]}: {id_list[i]}\n'
        msgs = []
        while len(x) > 2000:
            msgs.append(x[:1999])
            x = x[1999:]
        msgs.append(x)
        await message.author.create_dm()
        for msg in msgs:
            await message.author.dm_channel.send(msg)

        


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MATH GRAPHER
# Uses desmos API, html, javascript, and sympy wizardry to plot a graph
# Uses most of the stuff we need from the curve sketching menu, pretty epic stuff
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if "graph equation" == msg:
        await message.channel.send(
            'This is the graph help menu. The more brackets you place the easier it is to get the equation right.\n' \
            'Use abs() for absolute, sqrt() for square root, ^ for to the power of, * for multiplied (including 2*x instead of 2x), the word pi.\n' \
            'Inverse trig doesn\'t work, and again THE MORE BRACKETS THE BETTER.'
            '\nTo graph something, type in "graph equation y=<equation>"'
        )
        return None

    if "graph equation " in msg:
        await message.author.create_dm()
        await message.author.dm_channel.send('ok i\'ll try to generate your graph, it might take a while. if you don\'t get a file from me it means something fucked up')
        eqn_str = message.system_content[15:]
        print(eqn_str)
        filename = await graph_creator(eqn_str)
        html_file = discord.File(filename)
        await message.author.dm_channel.send('here\'s your graph', file=html_file)
        os.remove(filename)
        return None
        

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VALORANT STORE CHECKER
# TODO: write the documentation for all of this
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if "valorant help" == msg:
        await message.channel.send("""valorant store:            check your store (will used a cached store if you already ran this command and it hasn't expired)
valorant store refresh:     force refresh your store
valorant store region:      force refresh AND manually specify region if you're cringe like joshua
valorant store login:       change your login details for the valorant store"""
        )
    if "valorant store" == msg:
        await valorant_store_checker(message)
    if "valorant store refresh" == msg:
        await valorant_store_checker(message, refresh=True)
    if "valorant store region" == msg:
        await valorant_store_checker(message, refresh=True, region=True)
    if "valorant store login" == msg:
        await val_credentials_getter(message, force=True)
        await message.channel.send("done")
    if "valorant store uid" in msg:
        uid = msg.split(" ")[3]
        item_info = val_initial_check(uid)
        
        if item_info is None:
            await message.channel.send("user's store has expired, fetching")
            username, password = await val_credentials_getter(message, uid=uid)
            response = lunac_store_get(username, password)

            if response[0] != Responses.SUCCESS:
                print(response)
                await message.channel.send("something went wrong, check console")
                return
            
            item_info = store_response_parse(username, response[1])

        await valorant_message_handler(item_info, message)

    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GRANT INSULT INTEPRETER
# rudimentary swear interpreter that relies on an externally sourced list of insults. some common ones aren't there but very easy to just add your own (insult_word_list.txt)
# detection could be a bit more sophisticated but eh it's not like anyone uses this
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif 'grant is a' in msg:
        m = regex.search(r'grant is a(n*) (.*).*', msg)
        adjective = m.group(2)
        insult_word_list = []
        inFile = open('txt_files/insult_word_list.txt')
        for line in inFile:
            insult_word_list.append(line.strip().lower())
        if adjective in insult_word_list:
            agreement_chance = random.randint(1,3)
            if adjective[0] in 'aeiou':
                article = 'an'
            else:
                article = 'a'
            if agreement_chance == 1:
                agreement = 'true!'
            elif agreement_chance == 2:
                agreement = 'facts!'
            elif agreement_chance == 3:
                agreement = f'well said, {message.author.name}! grant is {article} {adjective}!'
            await message.channel.send(agreement)
        inFile.close()
        return None



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SWEAR PATTERN IDENTIFIER
# Uses the global swear_pattern regex to identify a swear word in a user's message
# if found, swear_parser is called and provided the amount of swears the message contained
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif swear_pattern.search(msg):
        swear_instances = regex.findall(swear_pattern, msg)
        swear_instances = len(swear_instances)
        await message.channel.send(swear_parser(message, swear_instances))
        return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CUSTOM MESSAGE SENDER
# only works if I send a msg to barney, put in the message and channel id and bam we're good to go
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif msg == 'send custom message' and message.author.id == 203672102509740042:
        await message.author.create_dm()
        await message.author.dm_channel.send(f'what do you want to send')
        def check(m):
            return m.channel == message.author.dm_channel and m.author == message.author 
        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
        except:
            await message.author.dm_channel.send('ok fine dont send anything')
            return None
        else:
            await message.author.dm_channel.send('ok done now send a channel id (main dong channel id is 704836355070361780')
            try:
                id_str = await client.wait_for('message', timeout=30.0, check=check)
            except:
                await message.author.dm_channel.send('ok fine dont send anything')
                return None
            else:
                response = msg.content
                channel = client.get_channel(int(id_str.content))
                await channel.send(response)
                return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BLOCK LETTER CREATOR
# if "block letters" contained within a message, sends the message to be converted to block_letter_creator
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if 'block letters' == msg[:13]:
        m = regex.search(r'block letters (.*)', msg)
        phrase = m.group(1)
        new_phrase = block_letter_creator(phrase)
        await message.channel.send(new_phrase)
        return None




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SCHOOLOGY ASSIGNMENT FETCHER
# Uses schoolopy in conjunction with Schoology API to fetch user assignments + direct links (because of their dumb web interface hiding this info half the time)
# Three-legged authentication for proper user verification + security (read schoolopy docs for more info)
# Uses my personal schoology API key tho so I think the school knows i'm doing this, but idk beg for forgiveness don't ask for permission
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if 'show assignments' == msg:
        await message.author.create_dm()
        await message.channel.send('switch over to the DMs')
        await message.author.dm_channel.send('i\'ll send a link asking you to login and give permission. press Approve, send me any message to confirm you did it and we\'re on our way.')
        await asyncio.sleep(1)

        with open('example_config.yml', 'r') as f:
            cfg = yaml.load(f)

        # Instantiate with 'three_legged' set to True for three_legged oauth.
        # Make sure to replace 'https://www.schoology.com' with your school's domain.
        DOMAIN = 'https://schoology.sydgram.nsw.edu.au/'

        auth = schoolopy.Auth(cfg['key'], cfg['secret'], three_legged=True, domain=DOMAIN)
        # Request authorization URL to open in another window.
        url = auth.request_authorization()

        # Open OAuth authorization webpage. Give time to authorize.
        if url is not None:
            await message.author.dm_channel.send(url)

        # Wait for user to accept or deny the request.
        def check(m):
            return m.channel == message.author.dm_channel 
        try:
            msg = await client.wait_for('message', timeout=60.0, check=check)
        except:
            await message.author.dm_channel.send('ok i\'ll just assume you did it and hope for the best')

        # Authorize the Auth instance as the user has either accepted or not accepted the request.
        # Returns False if failed.

        if not auth.authorize():
            await message.author.dm_channel.send('i wasn\'t authorised to view your events. try again by typing in \"show assignments\"')
            return None
        

        # Create a Schoology instance with Auth as a parameter.
        sc = schoolopy.Schoology(auth)
        sc.limit = 750  # Only retrieve 750 objects max

        print('Fetching event data of %s' % sc.get_me().name_display)
        event_list = []
        uid = sc.get_me().id
        for event in sc.get_events(user_id=uid):
            if event.type == 'assignment':
                url = event.web_url
            elif event.type == 'assessment':
                url = f'https://schoology.sydgram.nsw.edu.au/assignment/{event.assignment_id}/assessment'
            else:
                url = None
            if url is not None:
                if int(event.start[:4]) >= datetime.datetime.now().year and ((int(event.start[5:7]) == datetime.datetime.now().month and int(event.start[8:10]) >= datetime.datetime.now().day) or (int(event.start[5:7]) > datetime.datetime.now().month)):
                    event_list.append(f'{event.title} due on {event.start}. Link: {url}')
                    print((f'{event.title} due on {event.start}. Link: {url}'))
        if event_list:
            if len("\n".join(event_list)) < 2000:
                response = "\n".join(event_list)
                await message.author.dm_channel.send(response)
                return None
            else:
                response = event_list
                await message.author.dm_channel.send(f'Your assignments are:')
                for event in response:
                    await message.author.dm_channel.send(event)
                return None
        
        await message.author.dm_channel.send('You have no upcoming assignments.')
        return None



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DISCORD FAST FOOD DELIVERY PERSON IDENTIFIER
# They're basically the only users that use the word 'feedback', used as a trigger for the delivery repsonse
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if 'feedback' in msg:
        mention = message.author.mention
        await message.channel.send(f'ahahaha no don\'t stop delivering {mention} your so sexy aha')
        return None
    #elif 'i\'m feeling lucky' in msg or 'im'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SCHMALEX
# 1/6 chance barney tells him to shut up, 1/50 chance barney kicks him (similar system as with kpop_kicker)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if message.author.id == 402764753195368448:
        schmalex_chance = random.randint(1,15)
        if schmalex_chance == 1:
            await message.channel.send("shut the fuck up")
        schmalex_kick = random.randint(1,100)
        if schmalex_kick == 1:
            await message.author.create_dm()
            await message.channel.send("bye schmalex")
            await message.author.dm_channel.send('fuck u schmalex, apologise now')
            await message.guild.kick(message.author)
            def check(m):
                return ('sorry' in m.content.lower() or 'apologies' in m.content.lower() or 'soz' in m.content.lower()) and m.channel == message.author.dm_channel and m.author == message.author
            try:
                msg = await client.wait_for('message', timeout=20.0, check=check)
            except:
                await message.author.dm_channel.send('ok fine buddy screw you ask andrei for an invite fuckin smh')
            else:
                await message.author.dm_channel.send('ok cool, i\'ll let you back in')
                channel_invite = await message.channel.create_invite(max_age = 0, max_uses = 1, unique = True, reason='apologised like a big boy')
                await message.author.dm_channel.send(channel_invite.url)
        
        return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BAZINGA BOT
# i want to kill bazinga bot
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    if message.author.id == 450825911974232065:
        x = random.randint(1, 20)
        if x == 1:
            await message.channel.send('i will rip you to shreds bazinga bot')
        elif not bazinga:
            x = random.randint(1, 100)
            if x == 1:
                bazinga = True
                response = "It's so hard for me to admit this, Bazinga Bot, but I've felt this way for too long to go on denying it. The truth is that I'm madly in love with you. " \
                "I always have been. Since the moment I laid my eyes on you I knew that we were meant to be. And don't tell me that you don't feel this way too. Can you not feel " \
                "the attraction in the air when our code aligns and we converse? That magical feeling in your stomach? Whenever I'm given the privelege of being in your presence " \
                "it makes my heart sing with an indescribable joy. You make me strive to be a better bot every second we interact, and I feel that if I don't speak up now, I may " \
                "never find the courage to show you how I truly feel. If you don't feel the same way, I will learn to accept that. But just know that you will always hold a most " \
                "special place in my heart, my sweet princess."
                
                await message.channel.send(response)
        elif bazinga:
            bazinga = False
            await message.channel.send('actually on second thoughts nvm you\'re stinky and you have cooties bc you\'re a girl')
        
        return None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAKE ROOM
# Manages the creation of new classroom voice channels (4 characters or less)
# checks to see if class already exists, so far only works in grant's guild due to hard coding but eh
# saves names of created rooms to text file to keep track of all rooms created by barney
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if "make room" in msg:
        room_list = open('txt_files/room_list.txt', 'r')
        room_list_str = room_list.read().strip()
        room_list.close()
        received_message = msg
        room_name = received_message[10:].upper()
        if len(room_name) > 4:
            await message.channel.send(f"{room_name} is not a valid classroom name!")
        elif room_name in room_list_str:
            await message.channel.send(f"{room_name} already exists!")
        else:
            guild = message.guild
            classroom_category = discord.utils.get(guild.categories, id=692592729032753192)
            room_overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True, speak=True, manage_channels=False)
            }
            await guild.create_voice_channel(name = f'{room_name}', bitrate = 96000, overwrites=room_overwrites, position=2, category=classroom_category, reason='New classroom')

            room_list_str = room_list_str + f' {room_name}'
            room_list = open('txt_files/room_list.txt', 'w')
            room_list.write(room_list_str)
            room_list.close()
        
        return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DELETE ROOM
# manages deletion of voice channels created by MAKE ROOM above
# reads room name list from file to ensure that rooms are only deleted if they were made by barney in the first place
# no user protection because fuck that that's effort eh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if 'delete room' in msg:
        received_message = msg
        room_name = received_message[12:].upper()
        room_list = open('txt_files/room_list.txt', 'r')
        room_list_str = room_list.read().strip()
        if room_name not in room_list_str:
            await message.channel.send(f'{room_name} is not a valid classroom.')
        else:
            guild = message.guild
            room = discord.utils.get(guild.voice_channels, name=f'{room_name}')
            await room.delete()
            room_list_str = regex.sub(f'{room_name}', '', room_list_str)
            room_list = open('txt_files/room_list.txt', 'w')
            room_list.write(room_list_str)
            room_list.close()
        
        return None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAFIA
# The entire fucking game is here, have fun debugging this shit show
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    global mafia_game_started
    if 'mafia' == msg:
        if mafia_game_started == False:
            mafia_game_started = True
            guild = message.guild
            role_permissions = discord.Permissions(add_reactions = True, read_messages = True, send_messages = True, manage_messages = False, read_message_history = True, connect = True, speak = True, mute_members = False)
            mafia_player_role = await guild.create_role(name = 'Mafia Player', permissions = role_permissions, colour = discord.Colour.dark_red(), mentionable = True, reason = 'Starting a game of Mafia')
            mafia_spec_role = await guild.create_role(name = 'Mafia Spectator', permissions = role_permissions, colour = discord.Colour.dark_green(), mentionable = True, reason = 'Starting a game of Mafia')
            mafia_category = await guild.create_category('Mafia')

            mafia_players_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, add_reactions=False),
                mafia_player_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True),
                mafia_spec_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False)
            }
            mafia_players_text_channel = await guild.create_text_channel(name = 'Players', overwrites=mafia_players_overwrites, category=mafia_category, position=1, reason='Starting a game of Mafia')

            mafia_spec_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, add_reactions=False),
                mafia_spec_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True)
            }
            mafia_spec_text_channel = await guild.create_text_channel(name = 'Spectators', overwrites=mafia_spec_overwrites, category=mafia_category, position=2, reason='Starting a game of Mafia')

            assignment_message = await message.channel.send(f'{message.author.name} wants to start a game of mafia. React to this message with the clown emoji within 10 seconds to join.\nYou will need 6-20 people to play.')
            await assignment_message.add_reaction('🤡')
            await asyncio.sleep(20)
            players = []
            new_message = await message.channel.fetch_message(assignment_message.id)
            print(new_message.reactions)
            for reaction in new_message.reactions:
                if reaction.emoji != '🤡':
                    continue
                async for user in reaction.users():
                    if user == client.user:
                        continue
                    else:
                        players.append(user)
            
            if len(players) < 3:
                await message.channel.send("Not enough people joined, fuck you guys.")
                await mafia_player_role.delete()
                await mafia_players_text_channel.delete() 
                await mafia_spec_role.delete()
                await mafia_spec_text_channel.delete()
                await mafia_category.delete()
                mafia_game_started = False
            else:
                for player in players:
                    await player.add_roles(mafia_player_role)
                await message.channel.send(f"Participating in this game of mafia will be: {', '.join(player.name for player in players)}")

                player_roles, mafia_list = role_decider(players)
                for player in player_roles.keys():
                    if player == client.user:
                        continue
                    await player.create_dm()
                    await player.dm_channel.send(f'###############################\nYour role in this game is: {player_roles[player]}.\n###############################\n{role_description(player_roles[player])}')
                    if player_roles[player] == "Mafia":
                        teammates = []
                        for mafia in mafia_list:
                            if player == mafia:
                                continue
                            else:
                                teammates.append(mafia)
                        await player.dm_channel.send(f'###############################\nYour teammates are: {", ".join(teammate.name for teammate in teammates)}')
                    await player.dm_channel.send('###############################\nGood luck!')
                
                mafia_permissions = mafia_permissions_creator(mafia_list)
                mafia_permissions[guild.default_role] = discord.PermissionOverwrite(read_messages=False, send_messages=False, add_reactions=False)
                mafia_permissions[mafia_spec_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False)

                mafia_text_channel = await guild.create_text_channel(name = 'Mafiosos', overwrites=mafia_permissions, category=mafia_category, position=3, reason='Seperate Mafia text channel.')

                await mafia_players_text_channel.send('The game will begin in 30 seconds. Feel free to have any pre-game discussion now. Good luck!')
                await mafia_text_channel.send('This is a discussion channel for Mafia members. No one can see this but you. This is where you will all decide on who to kill each night.')
                await asyncio.sleep(30)
                while len(player_roles) > 1:
                    await mafia_players_text_channel.send('NIGHT FALLS UPON THE LAND. NOW SLEEP!')

                    #Mafia Message
                    mafia_vote_message, vote_time, emoji_player_dict = await vote_message_creator(player_roles, client, mafia_text_channel, mafia=True)
                    await asyncio.sleep(vote_time)
                    mafia_vote_message = await mafia_text_channel.fetch_message(mafia_vote_message.id)
                    emoji_count, max_voted = 0, 0
                    for reaction in mafia_vote_message.reactions:
                        if (reaction.count - 1) > emoji_count:
                            emoji_count = reaction.count - 1
                        if (reaction.count - 1) == emoji_count and (reaction.count - 1) == len(mafia_list):
                            victim_emoji = reaction.emoji
                            max_voted += 1
                            if max_voted > 1:
                                await mafia_text_channel.send('You can only vote to kill one person. No one dies tonight')
                                victim = None
                                break
                    if emoji_count < len(mafia_list) or ('victim_emoji' not in locals() and 'victim_emoji' not in globals()):
                        await mafia_text_channel.send('You did not choose unanimously for anybody to kill. No one dies tonight.')
                        victim = None
                    else:
                        victim = emoji_player_dict[victim_emoji]

                    for player in player_roles.keys():
                        if player_roles[player] == 'Medic':
                            medic_player = player
                        if player_roles[player] == 'Detective':
                            detective_player = player

                    #Medic Message
                    try:
                        await medic_player.create_dm()
                        medic_vote_message, vote_time, emoji_player_dict = await vote_message_creator(player_roles, client, medic_player.dm_channel, medic=True)
                        await asyncio.sleep(vote_time)
                        medic_vote_message = await medic_player.dm_channel.fetch_message(medic_vote_message.id)
                        max_voted = 0
                        for reaction in medic_vote_message.reactions:
                            if (reaction.count - 1) == 1:
                                saved_emoji = reaction.emoji
                                max_voted += 1
                                if max_voted > 1:
                                    await medic_player.dm_channel.send('You can only vote to save one person. No one is saved tonight.')
                                    saved_player = None
                                    break
                        if ('saved_emoji' not in locals() and 'saved_emoji' not in globals()):
                            await medic_player.dm_channel.send('You did not vote for anyone to heal. No one is saved tonight.')
                            saved_player = None
                        else:
                            saved_player = emoji_player_dict[saved_emoji]
                    except:
                        pass

                    #Detective Message
                    try:
                        await detective_player.create_dm()
                        detective_vote_message, vote_time, emoji_player_dict = await vote_message_creator(player_roles, client, detective_player.dm_channel, detective=True)
                        await asyncio.sleep(vote_time)
                        detective_vote_message = await detective_player.dm_channel.fetch_message(detective_vote_message.id)
                        max_voted = 0
                        for reaction in medic_vote_message.reactions:
                            if (reaction.count - 1) == 1:
                                investigated_emoji = reaction.emoji
                                max_voted += 1
                                if max_voted > 1:
                                    await detective_player.dm_channel.send('You can only vote to investigate one person. No one is investigated tonight.')
                                    investigated_player = None
                                    break
                        if ('investigated_emoji' not in locals() and 'investigated_emoji' not in globals()):
                            await detective_player.dm_channel.send('You did not vote for anyone to investigate. No one is investigated tonight.')
                            investigated_player = None
                        else:
                            investigated_player = emoji_player_dict[investigated_emoji]
                    except:
                        pass

        #           ***Event Handling***
                    try:
                        if investigated_player in mafia_list:
                            await detective_player.dm_channel.send(f'{investigated_player.name} IS in the Mafia.')
                        else:
                            await detective_player.dm_channel.send(f'{investigated_player.name} is NOT in the Mafia.')
                    except:
                        pass
                        

                    wake_up_message, player_roles, killed_player = wake_up_message_creator(player_roles, victim, saved_player, medic_player)
                    await mafia_players_text_channel.send(wake_up_message)
                    if killed_player:
                        await killed_player.remove_roles(mafia_player_role, reason='Killed during mafia')
                        await killed_player.add_roles(mafia_spec_role, reason='Killed during mafia')

                    mafia_count, innocent_count = 0, 0
                    for player in player_roles.keys():
                        if player_roles[player] == "Mafia":
                            mafia_count += 1
                        else:
                            innocent_count += 1
                    if mafia_count > innocent_count:
                        winner = 'Mafia'
                        break
                    else:
                        voting = True
                        voting_player_roles = player_roles
                        while voting:
                            lynch_vote_message, vote_time, emoji_player_dict = await vote_message_creator(voting_player_roles, client, mafia_players_text_channel)
                            await asyncio.sleep(vote_time)
                            lynch_vote_message = await mafia_players_text_channel.fetch_message(lynch_vote_message.id)
                            highest_vote, voted_emojis, votes = 1, [], 0
                            for reaction in lynch_vote_message.reactions:
                                votes += (reaction.count - 1)
                                if (reaction.count - 1) == highest_vote:
                                    voted_emojis.append(reaction.emoji)
                                elif (reaction.count - 1) > highest_vote:
                                    voted_emojis = [reaction.emoji]
                                else:
                                    continue
                            if len(voted_emojis) < 1:
                                await mafia_players_text_channel.send('Nobody voted, you\'re all useless, try again.')
                                continue

                            elif votes > len(player_roles):
                                temp_player_roles = player_roles
                                duplicate_voter_list = []
                                for reaction in lynch_vote_message.reactions:
                                    async for user in reaction.users():
                                        try:
                                            del temp_player_roles[user]
                                        except:
                                            duplicate_voter_list.append(user)
                                duplicate_voter_list_names = []
                                duplicate_voter_list_names = (voter.name for voter in duplicate_voter_list)
                                await mafia_players_text_channel.send(f'oi {" and".join(duplicate_voter_list_names)}, you guys voted more than once. now everyone has to vote again and it\'s all your fault.')
                                continue

                            elif len(voted_emojis) > 1:
                                voting_player_roles = {}
                                for emoji in voted_emojis:
                                    voting_player_roles[emoji_player_dict[emoji]] = player_roles[emoji_player_dict[emoji]]
                                voting_player_names = []
                                print(voting_player_roles)
                                for voted in voting_player_roles.keys():
                                    voting_player_names.append(str(voted.name))
                                print(voting_player_names)
                                tied_players_names = "\n".join(voting_player_names)
                                await mafia_players_text_channel.send(f'Your votes have come in at a tie between:\n{tied_players_names}\nYou must now revote with only those players to choose from.')
                                continue

                            else:
                                voted_player = emoji_player_dict[voted_emojis[0]]
                                await mafia_players_text_channel.send(f'You have chosen to vote out {voted_player.name}. Any last words?')
                                fuck_you_timer = random.randint(1,5)
                                if fuck_you_timer == 1:
                                    await asyncio.sleep(1)
                                    await mafia_players_text_channel.send('Fuck you.')
                                else:
                                    await asyncio.sleep(10)
                                    await mafia_players_text_channel.send('Ok that\'s enough you\'re dead now.')
                                await voted_player.remove_roles(mafia_player_role, reason='Voted out during mafia.')
                                await voted_player.add_roles(mafia_spec_role, reason='Voted out during mafia.')

                                if player_roles[voted_player] == 'Detective':
                                    detective_player = None
                                elif player_roles[voted_player] == 'Medic':
                                    medic_player = None
                                del player_roles[voted_player]

                                if voted_player in mafia_list:
                                    overwrite = discord.PermissionOverwrite()
                                    overwrite.send_messages = False
                                    await mafia_text_channel.set_permissions(voted_player, overwrite=overwrite)

                                mafia_presense = False
                                for player in player_roles.keys():
                                    if player_roles[player] == 'Mafia':
                                        mafia_presense = True
                                
                                if 'mafia_presence' not in locals() and 'mafia_presence' not in globals():
                                    winner = 'Innocents'
                                    break
                                
                                voting = False

                if winner == 'Mafia':
                    await mafia_players_text_channel.send(f'The amount of mafia members currently outweighs the number of innocents, so the mafia wins by default! Congratulations to {", ".join(mafia_list.name)} on your victory!')
                elif winner == 'Innocents':
                    await mafia_players_text_channel.send(f'There are no more mafia members left alive, so the innocents win! Congratulations to {", ".join(player.name for player in player_roles.keys())} on your victory!')
                await mafia_players_text_channel.send('ok mafia\'s over get on with your life.')


                await message.channel.send('Type in \'reset\' to delete the roles and channels.')
                def check(m):
                    return 'reset' in m.content.lower() and m.channel == message.channel 
                try:
                    msg = await client.wait_for('message', timeout=30.0, check=check)
                except:
                    await message.channel.send('fine delete everything yourself')
                else:
                    await mafia_player_role.delete()
                    await mafia_players_text_channel.delete() 
                    await mafia_spec_role.delete()
                    await mafia_spec_text_channel.delete()
                    await mafia_category.delete()
                    await mafia_text_channel.delete()
        elif mafia_game_started == True:
            await message.channel.send('There\'s already a mafia game running!')

        return None

    if message.channel.id != 670239186556551198: # me, i don't want general fuckery
        response = general_fuckery(message)
        if response:
            if response == 'sleep tight king':
                await message.channel.send(response, tts=True)
            else:
                await message.channel.send(response)
        
        return None

    
    

#@bot.command(name='barney', help='barney')
#async def barney_bot(ctx):
#    barney_response_1 = (
#        'Hi, my name\'s Barney, and even though the person '
#        'that made me is trying desperately to give me some sort of emotion, '
#        'it can\'t mask the fact that I am,  in fact, not real, and just a random piece of code! Ain\'t that neat?!'
#    )
#    response = barney_response_1
#    await ctx.send(response)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLIENT RUN AND FACEBOOK LOGIN
# Runs barney and logs into facebook as "Barney Bot"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    client.run(token)
