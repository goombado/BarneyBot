import os
import json
import discord
from discord.ext import commands
import random
import re
import time
import threading
import asyncio
import math
import copy

token = 'token i barely know er'
GUILD = '670124015339438081'

client = discord.Client()
bot = commands.Bot(command_prefix='!')
mafia_game_started = False


async def delete_everything(*stuff):
    for item in stuff:
        await item.delete()


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

def mafia_permissions_creator(mafia_list):
    mafia_permissions = {}
    for mafia in mafia_list:
        mafia_permissions[mafia] = discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True)
    return mafia_permissions


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




@client.event
async def on_message(message):
    if message.channel != client.get_channel(670124015775383572):
        return
    if message.author == client.user:
        return
    if message.guild.id == 210716706501296128:
        return
    global mafia_game_started
    if 'mafia' == message.content.lower():
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

                #Detective Message
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
                        
                        elif len(voted_emojis) > 1:
                            voting_player_roles = {}
                            for emoji in voted_emojis:
                                voting_player_roles[emoji_player_dict[emoji]] = player_roles[emoji_player_dict[emoji]]
                            voting_player_names = []
                            print(voting_player_roles)
                            voting_player_names.append(voted.name for voted in voting_player_roles.keys())
                            print(voting_player_names)
                            tied_players_names = "\n".join(voted.name for voted in voting_player_names)
                            await mafia_players_text_channel.send(f'Your votes have come in at a tie between:\n{tied_players_names}\nYou must now revote with only those players to choose from.')
                            continue

                        else:
                            voted_player = emoji_player_dict[voted_emojis[0]]
                            del player_roles[voted_player]
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
                await delete_everything(mafia_player_role, mafia_players_text_channel, mafia_spec_role, mafia_spec_text_channel, mafia_text_channel, mafia_category)
        elif mafia_game_started == True:
            await message.channel.send('There\'s already a mafia game running!')

client.run(token)