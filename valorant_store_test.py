from typing import Any, Dict, List, Tuple
from enum import Enum
import asyncio
import base64
import json
from datetime import datetime, timedelta
import discord
import requests
import rsa

my_uid = '203672102509740042'
calvin_uid = '470086166503489536'


class Responses(Enum):
    SUCCESS     = 0
    RATE_LIMIT  = 1
    TWO_FACTOR  = 2
    BAD_CODE    = 3


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



def initial_check(uid: str) -> Any:
    val_shop = val_shop_fetcher()

    if val_shop[uid] == 0:
        return None
    
    expired = datetime.strptime(val_shop[uid]["expiry"], "%d/%m/%Y %H:%M:%S") - datetime.now()
    secs = expired.total_seconds()

    if secs <= 0:
        return None
    
    return val_shop[uid]




def credentials_storer(val_details: Dict, user_id: str, username: str, password: str) -> Dict:
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



def credentials_query() -> Tuple:
    username = input("Username: ")
    password = input("Password: ")

    return username, password



def credentials_getter(user_id: str):
    val_details = val_details_fetcher()

    if val_details[user_id] == 0:
        username, password = credentials_query()
        credentials_storer(val_details, user_id, username, password)
    else:
        with open('private.key', 'r') as inFile:
            private = rsa.PrivateKey.load_pkcs1(inFile.read().encode('utf-8'))
        details = val_details.get(user_id)
        u_enc = base64.b64decode(details[0].encode())
        p_enc = base64.b64decode(details[1].encode())
        username = rsa.decrypt(u_enc, private).decode()
        password = rsa.decrypt(p_enc, private).decode()

    return username, password



def lunac_store_get(username: str, password: str) -> Tuple:
    u_b64 = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    p_b64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    headers = {
        'Origin': 'https://valorantstore.net',
        'Referer': 'https://valorantstore.net/'
    }

    r = requests.get(
        f'https://api.lunac.xyz/valorant/getPlayerStoreFront/{u_b64}/AP/{p_b64}',
        headers = headers
    )

    response = r.json()
    error = response.get("Error")

    if error is None:
        return (Responses.SUCCESS, response)
    elif error == "2fa":
        return (Responses.TWO_FACTOR, u_b64)
    else:
        return (Responses.RATE_LIMIT, None)



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



def get_2fa() -> str:
    code = input("2FA: ")
    return code



def lunac_store(username: str, password: str):
    response = lunac_store_get(username, password)
    err = response[0]
    
    if err == Responses.RATE_LIMIT:
        return err

    elif err == Responses.SUCCESS:
        return response[1]

    # 2FA is enabled, get code
    code = get_2fa()
    response = lunac_store_2fa(response[1], code)
    err = response[0]

    if err == Responses.BAD_CODE:
        return err
    
    return response[1]



def rate_limit_msg():
    print("too many requests, slow down")



def bad_code_msg():
    print("invalid 2FA code, try again from the beginnging")



def store_offer_getter() -> Any:
    r = requests.get("https://api.henrikdev.xyz/valorant/v1/store-offers")
    return r.json().get("data").get("Offers")



def skins_info_getter() -> Any:
    r = requests.get("https://valorant-api.com/v1/weapons/skins")
    return r.json().get("data")



def lunac_response_parse(username: str, response: Any) -> List:
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
    expiryDate = datetime.now() + timedelta(seconds = timeRemaining)
    expiryStr = expiryDate.strftime("%d/%m/%Y %H:%M:%S")
    item_info["expiry"] = expiryStr

    for i in range(len(relevant_offers)):
        name = relevant_skins[i].get("displayName")

        item_info["data"].append({
            "name":             name,
            "cost":             list(relevant_offers[i].get("Cost").values())[0],
            "icon":             relevant_skins[i].get("displayIcon"),
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

    

def embed_generator(item_info: dict, store: bool = True, levels: bool = True) -> discord.Embed:
    current = item_info["data"][item_info["index"]]
    
    if store:
        embed = discord.Embed(
            title = f"{item_info['username']}'s Store",
            type = "rich",
            description = f"The daily store page for {item_info['username']}.\n"\
                "⏪ ⏩ = Page Turn\n"\
                "ℹ️ = Info about current skin",
            colour=discord.Colour(0xfa4454)
        )
        embed.set_image(url=current["icon"])

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
        embed.add_field(name="Level", value=lvl["name"], inline=True)

        if lvl["video"] is not None:
            embed.add_field(name="Video", value=lvl["video"], inline=False)

    embed.add_field(name="Cost", value=str(current["cost"]), inline=True)
    embed.add_field(name="Expiry", value=item_info["expiry"], inline=True)
    return embed



def store_fetcher(uid: str):
    item_info = initial_check(uid)
    if item_info is not None:
        return item_info
    
    username, password = credentials_getter(uid)
    response = lunac_store(username, password)

    if response == Responses.RATE_LIMIT:
        rate_limit_msg()
        return
    elif response == Responses.BAD_CODE:
        bad_code_msg()
        return
    
    item_info = lunac_response_parse(username, response)
    val_shop = val_shop_fetcher()
    val_shop[uid] = item_info
    val_shop_saver(val_shop)

    return item_info


def reaction_list_gen(item_info: dict, store: bool = True, levels: bool = True) -> List:
    reaction_list = []

    if store:
        index = item_info["index"]
        reaction_list.append('ℹ️')
    elif levels:
        index = item_info["lvlIndex"]
        reaction_list.append('🎨')
        reaction_list.append('↩️')
    else:
        index = item_info["chromaIndex"]
        reaction_list.append('⬆️')
        reaction_list.append('↩️')

    if index == 0:
        reaction_list.insert(0, '⏩')
    elif index == (len(item_info["data"]) - 1):
        reaction_list.insert(0, '⏪')
    else:
        reaction_list.insert(0, '⏪')
        reaction_list.insert(1, '⏩')

    return reaction_list



# async def valorant_message_creator(item_info: dict, message: discord.Message, store: bool = True, levels: bool = True):
#     embed = embed_generator(item_info, store=store, levels=levels)
#     reaction_list = reaction_list_gen(item_info, store=store, levels=levels)

#     msg = await message.channel.send(embed=embed)
#     for emoji in reaction_list:
#         await msg.add_reaction(emoji)

#     def check(reaction, user):
#         return user == message.author and str(reaction.emoji) in reaction_list and reaction.message.id == msg.id
    
#     try:
#         reaction, __ = await client.wait_for('reaction_add', timeout=60.0, check=check)
#     except asyncio.TimeoutError:
#         return item_info, None, None
#     else:
#         react = str(reaction.emoji)

#         if react == '⏩':
#             item_info["index"] += 1
#             item_info["lvlIndex"] += 1
#             item_info["chromaIndex"] += 1
#         elif react == '⏪':
#             item_info["index"] -= 1
#             item_info["lvlIndex"] -= 1
#             item_info["chromaIndex"] -= 1
#         elif react == 'ℹ️':
#             store = False
#             levels = True
#         elif react == '↩️':
#             store = True
#             levels = True
#         elif react == '🎨':
#             levels = False

#         await msg.delete()
#         return item_info, store, levels


# async def valorant_message_handler(item_info: dict, message: discord.Message):
#     store = True
#     levels = True

#     while True:
#         item_info, store, levels = await valorant_message_creator(item_info, message, store, levels)
        
#         if item_info is None:
#             break



def store_checker(uid: str):
    item_info = store_fetcher(uid)
    with open("val_test_item_info.txt", 'w') as outFile:
        outFile.write(json.dumps(item_info, indent=4))
    # embed = embed_generator(item_info, store=True)
    # print(embed)



if __name__ == "__main__":
    store_checker(calvin_uid)