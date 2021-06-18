from SpamBot import *
from SpamBot.helpers.mongo import (
        add_user, user_already, get_all_users,
        add_chat, chat_already, get_all_chats
)
from SpamBot.plugins.eval import SUDO
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

p_btn = InlineKeyboardMarkup([
     [InlineKeyboardButton("Help And Commands ❓", callback_data="help")],
     [InlineKeyboardButton("Source Code 👨‍💻", url="https://github.com/TgxBotz/TelethonGPbot")]
     ])


PM_START_TEXT = """
**Hi {}**
I am a bot who works for @TheTelegramChats and can Detect Spammers in Groups Can Protect The Group

**Click the below button for getting help menu!**
"""

@nora.on_message(cmd("start"))
async def start(_, message):
    if message.chat.type != "private":
        await message.reply("Heya Nora Here :)")
    else:
        await message.reply(PM_START_TEXT.format(message.from_user.mention), reply_markup=p_btn)

group = 3
@nora.on_message(group=group)
async def lmoa(_, message):
    chat_id = message.chat.id
    is_served = await chat_already(chat_id)
    if not is_served:
        await add_chat(chat_id)
    if message.from_user:
        user_id = message.from_user.id
        is_served = await user_already(user_id)
        if not is_served:
            await add_user(user_id)

DIED = [1704673514]

@nora.on_message(
   cmd("stats")
   & filters.user(DIED)
)
async def stats(_, message):
    ok = await get_all_users()
    chats = await get_all_chats()
    text = f"""
<b>Nora Sᴛᴀᴛs:</b>

<b>Users:</b> {len(ok)}
<b>Chats:</b> {len(chats)}
"""

    await message.reply(text, parse_mode="HTML")

@nora.on_message(cmd("hemlo"))
async def hmkeiej(_, message):
    await message.reply('Died')

