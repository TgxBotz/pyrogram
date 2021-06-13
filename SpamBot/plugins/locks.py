from pyrogram import filters
from pyrogram.types import ChatPermissions
from SpamBot import *
from SpamBot.helpers.admins import adminsOnly
from telethon import events, Button
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

LOCKS_HELP = """
**✘ Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!**

‣ `?lock` - To lock a module in the chat.
‣ `?unlock` - To unlock a module in the chat.
‣ `?locktypes` - To get a list of modules can be locked
"""

"""
@nora.on_message(cmd("lock") & filters.group)
@adminsOnly
async def lock(perm, message):
    if not perm.can_change_info:
      await message.reply(
        "You are missing the following rights to use this command:CanChangeInfo"
      )
      return
    try:
       input = message.command[1]
    except IndexError:
       await message.reply("Give a string to lock!")
       return
    chat = message.chat.id
    if "all" in input:
      await nora.set_chat_permissions(chat, ChatPermissions())
      return
    elif "text" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_send_messages=False))
      return
    elif "game" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_send_games=False))
      return
    elif "inline" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_use_inline_bots=False))
      return
    elif "polls" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_polls=False))
       return
    elif "gif" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_animations=False))
       return
    elif "stickers" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_stickers=False))
       return
    elif "media" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_media_messages=False))
       return
    await message.reply(f"Succesfully Locked {input}")
      
@nora.on_message(cmd("unlock") & filters.group)
@adminsOnly
async def unlock(perm, message):
    if not perm.can_change_info:
      await message.reply(
        "You are missing the following rights to use this command:CanChangeInfo"
      )
      return
    try:
       input = message.command[1]
    except IndexError:
       await message.reply("Give a string to lock!")
       return
    chat = message.chat.id
    if "all" in input:
      await nora.set_chat_permissions(chat, ChatPermissions())
      return
    elif "text" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_send_messages=True))
      return
    elif "game" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_send_games=True))
      return
    elif "inline" in input:
      await nora.set_chat_permissions(chat, ChatPermissions(can_use_inline_bots=True))
      return
    elif "polls" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_polls=True))
       return
    elif "gif" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_animations=True))
       return
    elif "stickers" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_stickers=True))
       return
    elif "media" in input:
       await nora.set_chat_permissions(chat, ChatPermissions(can_send_media_messages=True))
       return
    await message.reply(f"Succesfully Unlocked {input}")

"""

@nora.on_message(cmd("locktypes"))
async def locktypes(_, message):
    TEXT = """
**Locks:**

‣ Text
‣ Media
‣ Sticker
‣ Gifs
‣ Videos
‣ Contacts
‣ Games
‣ Inline 
‣ all
"""
    await message.reply(TEXT)

@nora.on_callback_query(filters.regex("locks"))
async def _(client, cb):
    await cb.answer()
    await cb.edit_message_text(
     LOCKS_HELP,
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
        ]
      )
    )


