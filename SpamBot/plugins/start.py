from SpamBot import *
from telethon import events, Button
from SpamBot.plugins.sql.broadcast import *
from SpamBot.plugins.sql.chats import *
import SpamBot.plugins.sql.broadcast as sql
import SpamBot.plugins.sql.chats as chats
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

@nora.on_message(filters.private)
async def add_user(_, message):
    if not sql.is_user_in_db(int(message.from_user.id)):
        sql.add_new_user(int(message.from_user.id), int(1))
        return

DIED = [1704673514]

@nora.on_message(
   cmd("stats")
   & filters.user(DIED)
)
async def stats(_, message):
    ok = len(get_all_users())
    chats = len(get_all_chat_id())
    text = f"""
<b>Nora Sᴛᴀᴛs:</b>

<b>Users:</b> {ok}
<b>Chats:</b> {chats}
"""

    await message.reply(text, parse_mode="HTML")

@nora.on_message(filters.new_chat_members)
async def joined(client, message):
    text = f"""
I have been added to
`{message.chat.id}`
"""
    if message.new_chat_members[0].id == 1813724543:
       await nora.send_message(
         -1001457188670,
         text
       )
       return

@nora.on_message(cmd("hemlo"))
async def hmkeiej(_, message):
    await message.reply('Died')

