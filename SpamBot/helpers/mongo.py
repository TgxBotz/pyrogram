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
    
