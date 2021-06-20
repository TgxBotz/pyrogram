from .. import db
from typing import Dict, List, Union


""" Warnings Database! """
warnsdb = db.warns

async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id


async def get_warns_count() -> dict:
    chats = warnsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return {}
    chats_count = 0
    warns_count = 0
    for chat in await chats.to_list(length=100000000):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> Dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id}, {"$set": {"warns": warnsd}}, upsert=True
        )
        return True
    return False


""" NightMode Database! """
night_mode = db["NightMode"]


async def add_night_chat(chat_id):
    await night_mode.insert_one({"chat_id": chat_id})


async def rm_night_chat(chat_id):
    await night_mode.delete_one({"chat_id": chat_id})


async def get_all_night_chats():
    lol = [ujwal async for ujwal in night_mode.find({})]
    return lol


async def is_night_chat_in_db(chat_id):
    k = await night_mode.find_one({"chat_id": chat_id})
    if k:
        return True
    else:
        return False
    
""" Nsfw Database! """

nsfwdb = db["Nsfw"]

async def is_nsfw_on(chat_id: int) -> bool:
    chat = await nsfwdb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def nsfw_on(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if is_nsfw:
        return
    return await nsfwdb.delete_one({"chat_id": chat_id})


async def nsfw_off(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if not is_nsfw:
        return
    return await nsfwdb.insert_one({"chat_id": chat_id})


""" Flood Database! """
floodb = db["Flood"]

async def is_flood_on(chat_id: int) -> bool:
    chat = await floodb.find_one({"chat_id": chat_id})
    if not chat:
      return True
    return False

async def en_flood(chat_id: int):
    alre = await is_flood_on(chat_id)
    if alre:
        return
    await floodb.delete_one({"chat_id": chat_id})
    return

async def di_flood(chat_id: int):
    alre = await floodb.find_one({"chat_id": chat_id})
    if not alre:
        await floodb.insert_one({"chat_id": chat_id})
        return


""" Chats Databse! """
chatsdb = db["Chats"]

async def add_chat(chat_id: int):
    alre = await chat_already(chat_id)
    if alre:
        return
    await chatsdb.insert_one({"chat_id": chat_id})

async def chat_already(chat_id: int) -> bool:
    ok = chatsdb.find_one({"chat_id": chat_id})
    if not ok:
        return False
    return True

async def get_all_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list

""" Users DataBase  """

usersdb = db["Users"]

async def user_already(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_all_users() -> list:
    users = usersdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list

async def add_user(user_id: int):
    ok = await user_already(user_id)
    if ok:
        return
    await usersdb.insert_one({"user_id": user_id})


"""  Profanity DataBase! """

pdb = db["Profanity"]

async def is_pdb(chat_id: int) -> bool:
    chat = await pdb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False

async def add_pdb(chat_id: int):
    alre = await is_pdb(chat_id)
    if alre:
        return
    await pdb.delete_one({"chat_id": chat_id})
    return

async def rm_pdb(chat_id: int):
    alre = await is_pdb(chat_id)
    if not alre:
        return
    await pdb.insert_one({"chat_id": chat_id})
    return


"""  Sudos DataBase  """
sudodb = db["Sudos"]

async def add_sudo(user_id: int):
    alre = await already_sudo(user_id)
    if not alre:
        await sudodb.insert_one({"user_id": user_id})
        return

async def rm_sudo(user_id: int):
    alre = await already_sudo(user_id)
    if not alre:
        await sudodb.delete_one({"user_id": user_id})
        return

async def already_sudo(user_id: int) -> bool:
    ok = await sudodb.find_one({"user_id": user_id})
    if ok:
        return False
    return True

async def get_all_sudos() -> list:
    users = sudodb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list

""" Gbans DataBase! """

gbansdb = db["Gbans"]

async def gban_user(user_id: int):
    alre = await already_gbanned(user_id)
    if not alre:
        await gbansdb.insert_one({"user_id": user_id})
        return

async def ungban_user(user_id: int):
    alre = await already_gbanned(user_id)
    if not alre:
        await gbansdb.delete_one({"user_id": user_id})
        return

async def already_gbanned(user_id: int) -> bool:
    ok = gbansdb.find_one({"user_id": user_id})
    if ok:
        return False
    return True
