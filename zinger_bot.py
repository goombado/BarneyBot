import discord
from discord.ext import commands, tasks
import asyncio
import json
import discord.utils
from datetime import datetime
from barney import kpop_qr_creator, txt_populator
import os
import time
import datetime as dt


intents = discord.Intents.all()
client = discord.Client(intents=intents)

inFile = open('txt_files/zing_list.txt')
no_zing_list = json.loads(inFile.read())
inFile.close()

inFile = open('txt_files/daily_zing_scores.txt')
daily_zing_scores = json.loads(inFile.read())
inFile.close()

inFile = open('txt_files/zing_data.txt')
zing_data = json.loads(inFile.read())
inFile.close()

inFile = open('txt_files/all_time_zing_scores.txt')
all_time_zing_scores = json.loads(inFile.read())
inFile.close()

inFile = open('txt_files/zing_king_leaderboard.txt')
zing_king_leaderboard = json.loads(inFile.read())
inFile.close()

inFile = open('txt_files/zing_king_points.txt')
zing_king_points = json.loads(inFile.read())
inFile.close()


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



@client.event
async def on_ready():
    global zing_king_role
    global zing_data
    global daily_zing_scores
    global zing_king_leaderboard
    global guild
    global zing_king_points
    guild = discord.utils.get(client.guilds, id=210716706501296128)
    zing_king_role = discord.utils.get(guild.roles, id=739747974724452433)
    now = datetime.now()

    for member in guild.members:
        x=[]
        for role in member.roles:
            x.append(role.name)
        y=member.name + ': ' + ', '.join(x)
        print(y)

    if datetime.strptime(zing_data["day"], "%Y %m %d") < datetime.strptime(now.strftime("%Y %m %d"), "%Y %m %d"):

        for user in daily_zing_scores.keys():
            daily_zing_scores[user] = 0
        
        if zing_data["king"] != "0":
            zing_king_leaderboard[zing_data["king"]] += 1
            zing_king_points[zing_data["king"]] += 1
            current_king = guild.get_member(int(zing_data["king"]))
            await current_king.remove_roles(zing_king_role)

        zing_data["king"] = "0"
        zing_data["day"] = now.strftime("%Y %m %d")
        
        outFile = open("txt_files/zing_data.txt", 'w')
        outFile.write(json.dumps(zing_data, indent=4))
        outFile.close()

        outFile = open("txt_files/zing_king_leaderboard.txt", 'w')
        outFile.write(json.dumps(zing_king_leaderboard, indent=4))
        outFile.close()

        outFile = open("txt_files/zing_king_scores.txt", 'w')
        outFile.write(json.dumps(zing_king_leaderboard, indent=4))
        outFile.close()
        
        outFile = open('txt_files/daily_zing_scores.txt', 'w')
        outFile.write(json.dumps(daily_zing_scores, indent=4))
        inFile.close()

        outFile = open('txt_files/zing_king_points.txt', 'w')
        outFile.write(json.dumps(zing_king_points, indent=4))
        inFile.close()

    txt_populator('all_time_zing_scores.txt', client, '210716706501296128')
    txt_populator('daily_zing_scores.txt', client, '210716706501296128')
    txt_populator('zing_king_leaderboard.txt', client, '210716706501296128')
    txt_populator('zing_king_scores.txt', client, '210716706501296128')
    txt_populator('zing_king_points.txt', client, '210716706501296128')

    print('zinger bot is ready')
    


@client.event
async def on_message(message):
    global user_dict
    global no_zing_list
    global daily_zing_scores
    global all_time_zing_scores
    global zing_data
    global guild
    global zing_king_role
    global zing_king_leaderboard
    global zing_king_points

    if message.author == client.user:
        return
    

    msg = message.content.lower()
    msg2 = message.system_content.lower()

    if msg == 'zing me off':
        if message.author.id in no_zing_list:

            await message.channel.send('you\'re already zinged off')
        else:
            no_zing_list.append(message.author.id)
            outFile = open('txt_files/zing_list.txt', 'w')
            outFile.write(json.dumps(no_zing_list, indent=4))
            outFile.close()
            
            await message.channel.send('zinged off')

    elif msg == 'zing me on':
        if message.author.id not in no_zing_list:
            
            await message.channel.send('you\'re already zinged on')
        else:
            no_zing_list.remove(message.author.id)
            outFile = open('txt_files/zing_list.txt', 'w')
            outFile.write(json.dumps(no_zing_list, indent=4))
            outFile.close()
            
            await message.channel.send('zinged on')
    
    elif 'check zing score ' in msg:
        uid = msg[11:]
        user = guild.get_member(uid)
        await message.channel.send(f'daily zing score: {daily_zing_scores[str(uid)]}\nall time zing score: {all_time_zing_scores[str(uid)]}')

    elif msg == 'zing king stats':
        await message.channel.send(f'you have been zing king {zing_king_leaderboard[str(message.author.id)]} times, and have {zing_king_points[str(message.author.id)]} unredeemed zing king points.')


    elif 'redeem zing' == msg:
        await message.author.create_dm()
        await message.author.dm_channel.send('what would you like to use your points on (type the number of your selection)\n1. kpop coupon\n2. andrei buys you a zinger box (40 points)')
        
        
        def check(m):
            return m.author == message.author and (m.content in ['1', '2'])
        try:
            selection = await client.wait_for('message', timeout=20.0, check=check)
        except:
            await message.author.dm_channel.send('you took too long')
            return None
        else:
            pass

        if selection.content == '2':
            point_dif = zing_king_points[str(message.author.id)] - 40
            if point_dif < 0:
                await message.author.dm_channel.send(f'you don\'t have enough points, you need {abs(point_dif)} more points')
                return None
            
            zing_king_points[str(message.author.id)] -= 40
            outFile = open('txt_files/zing_king_points.txt', 'w')
            outFile.write(json.dumps(zing_king_points, indent=4))
            outFile.close()

            outFile = open(f'zing_box_{time.time()}.txt', 'w')
            outFile.write(f'box redeemed at {time.time()} by {message.author.id} - {user_dict[message.author.id]}')
            outFile.close()
            await message.author.dm_channel.send(f'ok done message andrei to verify the zinger box.')
            return None

        else:
            await message.author.dm_channel.send('what coupon?\n1. 24 hours (10 points)\n2. 3 days (25 points)\n3. 7 days (50 points)')

            def check(m):
                return m.author == message.author and (m.content in ['1', '2', '3', '4'])
            try:
                template = await client.wait_for('message', timeout=20.0, check=check)
            except:
                await message.author.dm_channel.send('you took too long')
                return None
            else:
                qr_dict = {'1': ['24_hours', 6, '24 hour'], 
                '2': ['3_days', 15, '3 day'], 
                '3': ['7_days', 25, '7 day'], 
                }
            point_dif = zing_king_points[str(message.author.id)] - qr_dict[template.content][1]
            if point_dif < 0:
                await message.author.dm_channel.send(f'you don\'t have enough points, you need {abs(point_dif)} more points')
                return None

            zing_king_points[str(message.author.id)] -= qr_dict[template.content][1]
            outFile = open('txt_files/zing_king_points.txt', 'w')
            outFile.write(json.dumps(zing_king_points, indent=4))
            outFile.close()

            await message.author.dm_channel.send(f'ok making a {qr_dict[template.content][2]} qr code')
            file_name = kpop_qr_creator(qr_dict[template.content][0], return_file=True)
            coupon = discord.File(file_name)
            await message.author.dm_channel.send(f'here\'s your kpop coupon, use it wisely', file=coupon)
            os.remove(file_name)


    elif msg == 'zing leaderboard':
        if not message.guild:
            return
        if message.guild.id != 210716706501296128:
            await message.channel.send('You can only request a leaderboard in the main server')
            return
        
        embed_template_scores_daily = discord.Embed(
            title='Zing Leaderboard',
            type='rich',
            description='The daily zing scores of everybody in the server.\n👑 = Zing King Leaderboard\n🇦 = All Time Leaderboard\n⏪ ⏩ = Page Turn\nIf the buttons don\'t work, type in "zing leaderboard" again.',
            colour=discord.Colour(0xd31212)
        )

        embed_template_scores_alltime = discord.Embed(
            title='Zing Leaderboard',
            type='rich',
            description='The all time zing scores of everybody in the server.\n👑 = Zing King Leaderboard\n🇩 = Daily Leaderboard\n⏪ ⏩ = Page Turn\nIf the buttons don\'t work, type in "zing leaderboard" again.',
            colour=discord.Colour(0xd31212)
        )

        embed_template_king = discord.Embed(
            title='Zing Leaderboard',
            type='rich',
            description='The zing king scores of everybody in the server.\n🇦 = All Time Leaderboard\n🇩 = Daily Leaderboard\n⏪ ⏩ = Page Turn\nIf the buttons don\'t work, type in "zing leaderboard" again.',
            colour=discord.Colour(0xd31212)
        )
        
        # embed.set_author(name='Zinger Bot', url='https://kfc.com.au')

        def dict_sorter(message, data):
            global user_dict
            unsorted = {}
            for member in message.guild.members:
                try:
                    unsorted[(user_dict[member.id] if member.id in user_dict.keys() else member.name)] = data[str(member.id)]
                except:
                    continue
            
            names_sorted = sorted(unsorted.items(), key=lambda x: (-x[1],x[0]))

            i=j=0
            pageified = {}
            for rank in names_sorted:
                if i%9==0:
                    i+=1
                    j+=1
                    pageified[j] = []
                if i%9!=0:
                    i+=1
                    pageified[j].append(rank)
            
            return pageified


        zing_all_time = dict_sorter(message, all_time_zing_scores)
        zing_daily = dict_sorter(message, daily_zing_scores)
        zing_king_all_time = dict_sorter(message, zing_king_leaderboard)


        
        async def message_handler(embed, message, data, zing_data):
            name_list = '\n'.join([x[0] for x in zing_data[data['index']]])
            score_list = '\n'.join([str(x[1]) for x in zing_data[data['index']]])
            embed.add_field(name='Names', value=name_list, inline=True)
            embed.add_field(
                name = ('Daily Scores' if data['type'] == 'daily scores' else 'King Scores' if data['type'] == 'king scores' else 'All Time Scores'),
                value=score_list, inline=True
            )
            reaction_list = []
            if data['index'] != 1:
                reaction_list.append('⏪')
            if data['index'] != len(zing_data):
                reaction_list.append('⏩')
            if data['type'] == 'daily scores':
                reaction_list.extend(['👑', '🇦'])
            if data['type'] == 'all time scores':
                reaction_list.extend(['👑', '🇩'])
            if data['type'] == 'king scores':
                reaction_list.extend(['🇩', '🇦'])

            msg = await message.channel.send(embed=embed)
            for emoji in reaction_list:
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user != client.user and user == message.author and str(reaction.emoji) in reaction_list and reaction.message.id == msg.id
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                return False
            else:
                if str(reaction.emoji) == '⏩':
                    data['index'] += 1
                elif str(reaction.emoji) == '⏪':
                    data['index'] -= 1
                elif str(reaction.emoji) == '👑':
                    data['index'] = 1
                    data['type'] = 'king scores'
                elif str(reaction.emoji) == '🇦':
                    data['index'] = 1
                    data['type'] = 'all time scores'
                elif str(reaction.emoji) == '🇩':
                    data['index'] = 1
                    data['type'] = 'daily scores'

                await msg.delete()
                return data
        
        data = {'index': 1, 'type': 'all time scores'}
        while True:
            if data['type'] == 'daily scores':
                while data['type'] == 'daily scores':
                    embed = embed_template_scores_daily.copy()
                    data = await message_handler(embed, message, data, zing_daily)
                    if not data:
                        return
            elif data['type'] == 'all time scores':
                while data['type'] == 'all time scores':
                    embed = embed_template_scores_alltime.copy()
                    data = await message_handler(embed, message, data, zing_all_time)
                    if not data:
                        return
            elif data['type'] == 'king scores':
                while data['type'] == 'king scores':
                    embed = embed_template_king.copy()
                    data = await message_handler(embed, message, data, zing_king_all_time)
                    if not data:
                        return
            





    elif ('z' in msg or '2' in msg or '🇿' in msg) and ('i' in msg or '1' in msg or 'l' in msg or '🇮' in msg) and ('n' in msg or '🇳' in msg) and ('g' in msg or '9' in msg or '🇬' in msg) and message.author.id not in no_zing_list:
        usr = user_dict.get(message.author.id, False)
        if usr:
            
            await message.channel.send(f'zing on {usr}')
        else:
            
            await message.channel.send('zing on')
        
        daily_zing_scores[str(message.author.id)] += 1
        all_time_zing_scores[str(message.author.id)] += 1

        if daily_zing_scores[str(message.author.id)] > daily_zing_scores[zing_data["king"]]:
            if zing_data["king"] != "0":
                current_king = message.guild.get_member(int(zing_data["king"]))
                await current_king.remove_roles(zing_king_role, reason='the king has been dethroned')

            new_king = message.guild.get_member(message.author.id)
            await new_king.add_roles(zing_king_role, reason='long live the king')


            zing_data["king"] = str(message.author.id)
            outFile = open('txt_files/zing_data.txt', 'w')
            outFile.write(json.dumps(zing_data, indent=4))
            outFile.close()

        outFile = open('txt_files/daily_zing_scores.txt', 'w')
        outFile.write(json.dumps(daily_zing_scores, indent=4))
        outFile.close()

        outFile = open('txt_files/all_time_zing_scores.txt', 'w')
        outFile.write(json.dumps(all_time_zing_scores, indent=4))
        outFile.close()

        

    if message.guild:
        if message.guild.id == 210716706501296128:
            return
    if message.author.id in user_dict:
        print(msg)
        print(f'sent by: {user_dict[message.author.id]}')
    else:
        print(msg)
        print(f'sent by: {message.author.name}')


client.run('zing on')