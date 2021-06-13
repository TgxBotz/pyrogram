from pyrogram import filters
from SpamBot import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import functools

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

@nora.on_callback_query(filters.regex("misc"))
async def misc(client, cb):
    await cb.answer()
    await cb.edit_message_text(MISC_HELP, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
      ]
     )
    )
