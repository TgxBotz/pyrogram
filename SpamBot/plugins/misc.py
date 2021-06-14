from pyrogram import filters
from SpamBot import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatPermissions
import functools
from time import time

MISC_HELP = """
**✘ An "odds and ends" module for small, simple commands which don't really fit anywhere.**

‣ `?ping` - To get ping status.
‣ `?meme` - To create a meme.
‣ `?chatinfo` - To get the group info.
‣ `?id` - To get current chat id or replied user id.
‣ `?info` - To get info of a user.
"""


async def hmm(message):
    if message.reply_to_message.media:
      ok = message.reply_to_message.media
      if "sticker" in ok:
        fileid = message.reply_to_message.sticker.file_id
        ufile = message.reply_to_message.sticker.file_unique_id
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`\n\n**● File-Type:** `{}`\n📁 **File-ID:** `{}`\n📂 **File-Unique-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.media, message.reply_to_message.sticker.file_id, message.reply_to_message.sticker.file_unique_id))
      elif "photo" in ok:
        fileid = message.reply_to_message.photo.file_id
        ufile = message.reply_to_message.photo.file_unique_id
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`\n\n**● File-Type:** `{}`\n📁 **File-ID:** `{}`\n📂 **File-Unique-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.media, message.reply_to_message.photo.file_id, message.reply_to_message.photo.file_unique_id))
      elif "animation" in ok:
        fileid = message.reply_to_message.animation.file_id
        ufile = message.reply_to_message.animation.file_unique_id
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`\n\n**● File-Type:** `{}`\n📁 **File-ID:** `{}`\n📂 **File-Unique-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.media, message.reply_to_message.animation.file_id, message.reply_to_message.animation.file_unique_id))
      elif "document" in ok:
        fileid = message.reply_to_message.document.file_id
        ufile = message.reply_to_message.document.file_unique_id
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`\n\n**● File-Type:** `{}`\n📁.**File-ID:** `{}`\n📂 **File-Unique-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.media, message.reply_to_message.document.file_id, message.reply_to_message.document.file_unique_id))
      elif "audio" in ok:
        fileid = message.reply_to_message.audio.file_id
        ufile = message.reply_to_message.audio.file_unique_id
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`\n\n**● File-Type:** `{}`\n📁 **File-ID:** `{}`\n📂 **File-Unique-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id, message.reply_to_message.media, message.reply_to_message.audio.file_id, message.reply_to_message.audio.file_unique_id))
    elif message.reply_to_message.forward_from_chat:
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **{}-ID:** `{}`\n**Chat-Type:** `{}`".format(message.reply_to_message.from_user.id, message.reply_to_message.forward_from_chat.title, message.reply_to_message.forward_from_chat.id, message.reply_to_message.forward_from_chat.type))
    else:
        text = await message.reply("👥 **User-ID:** `{}`\n🗨️ **Chat-ID:** `{}`".format(message.reply_to_message.from_user.id, message.chat.id))

    return text
    
def id_wrap(func):
    @functools.wraps(func)
    async def hn(client, message):
      if message.reply_to_message:
          await hmm(message)
      else:
          await func(client, message)
    return hn

@nora.on_message(cmd("id"))
@id_wrap
async def id(_, message):

    if not message.reply_to_message:
        await message.reply("**ID:** `{}`\n**Chat-ID:** `{}`".format(message.from_user.id, message.chat.id))
        return
    if len(message.command) != 1:
        ok = message.text.split(None, 1)[1]
        try:
           user_id = await nora.get_users(ok)
        except BaseException as be:
           await message.reply(f"**Error:**\n`{be}`")
           return
        await message.reply("**{}-ID:** `{}`".format(
         user.first_name,
         user.id)
        )

async def list_admins(chat_id: int):
    list_of_admins = []
    async for member in nora.iter_chat_members(
        chat_id, filter="administrators"
    ):
        list_of_admins.append(member.user.id)
    return list_of_admins

DB = {}
DEVS = [1704673514, 1157157702] 

def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0

flood_group = 14

@nora.on_message(
    ~filters.service
    & ~filters.me
    & ~filters.private
    & ~filters.channel
    & ~filters.bot
    & ~filters.edited,
    group=flood_group,
)
async def flood_control_func(_, message: Message):
    chat_id = message.chat.id

    # Initialize db if not already.
    if chat_id not in DB:
        DB[chat_id] = {}

    if not message.from_user:
        reset_flood(chat_id)
        return

    user_id = message.from_user.id
    mention = message.from_user.mention

    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    # Reset floodb of current chat if some other user sends a message
    reset_flood(chat_id, user_id)

    # Ignore devs and admins
    mods = (await list_admins(chat_id)) + DEVS
    if user_id in mods:
        return

    # Mute if user sends more than 7 messages in a row
    if DB[chat_id][user_id] >= 7:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=int(time() + 3600),
            )
        except Exception:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" Unmute  ",
                        callback_data=f"unmute_{user_id}",
                    )
                ]
            ]
        )
        return await message.reply_text(
            f"**Spammer:** {mention}",
            reply_markup=keyboard,
        )
    DB[chat_id][user_id] += 1


@nora.on_callback_query(filters.regex("misc"))
async def misc(client, cb):
    await cb.answer()
    await cb.edit_message_text(MISC_HELP, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
      ]
     )
    )
