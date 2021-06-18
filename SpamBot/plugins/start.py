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
async def add_user(_, message):
    ch_al = await chat_already(message.chat.id)
    if not ch_al:
        await add_chat(message.chat.id)
    if message.from_user:
      already = await user_already(message.from_user.id)
      if not already:
          await add_user(message.from_user.id)


DIED = [1704673514]

@nora.on_message(
   cmd("stats")
   & filters.user(DIED)
)
async def stats(_, message):
    ok = len(get_all_users())
    chats = len(get_all_chats())
    text = f"""
<b>Nora Sᴛᴀᴛs:</b>

<b>Users:</b> {ok}
<b>Chats:</b> {chats}
"""

    await message.reply(text, parse_mode="HTML")

@nora.on_message(cmd("hemlo"))
async def hmkeiej(_, message):
    await message.reply('Died')

