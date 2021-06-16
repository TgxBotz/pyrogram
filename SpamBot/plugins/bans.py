from SpamBot.helpers.admins import adminsOnly, selfadmin, admind_res
from .. import *
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SpamBot.helpers.wrappers import anon_check



BANS_TEXT = """
**✘ Some people need to be publicly banned; spammers, annoyances, or just trolls.**

‣ `?kickme` - To self Kick you from a chat.
‣ `?kick` - To kick someone from a chat.
‣ `?ban` - To Ban Someone from a chat.
‣ `?unban` - To Unban Someone from the chat.
‣ `?dban` - To delete the replied msg and bans the user.
‣ `?sban` - To delete the replied msg and kicks the user.
‣ `?skick` - To Delete Your msg and kicks the user 
‣ `?dkick` - To delete your msg and and kicks the replied user.
"""

@nora.on_callback_query(filters.regex("bans"))
async def _(client, cb):
    await cb.answer()
    await cb.edit_message_text(BANS_TEXT, reply_markup=InlineKeyboardMarkup([
       [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
      ]
    ))


@nora.on_message(cmd("ban") & filters.group)
@adminsOnly
@selfadmin
@anon_check()
async def ban(perm, message):
    if not perm.can_restrict_members:
       await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
       return
    if message.reply_to_message:
       user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
       user = message.text.split(" ", 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
       await message.reply("Reply to a user or give it's id/Username to ban him")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await nora.kick_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(user)
    await message.reply("Succesfully Banned {} in {}".format(info.mention, message.chat.title))

@nora.on_message(cmd("unban") & filters.group)
@adminsOnly
@selfadmin
async def ban(perm, message):
    if not perm.can_restrict_members:
       await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
       return
    if message.reply_to_message:
       user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
       user = message.text.split(" ", 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
       await message.reply("Reply to a user or give it's id/Username to ban him")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(user)
    await message.reply("Succesfully Unbanned {} in {}".format(info.mention, message.chat.title))

@nora.on_message(cmd("kick") & filters.group)
@adminsOnly
@selfadmin
async def kick(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
      return
    if message.reply_to_message:
       user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
       user = message.text.split(" ", 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
       await message.reply("Reply to a user or give it's id/Username to ban him")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await nora.kick_chat_member(message.chat.id, user) 
        await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(user)
    await message.reply("Succesfully Kicked {} in {}".format(info.mention, message.chat.title))

@nora.on_message(cmd("kickme") & filters.group)
@selfadmin
async def kickme(client, message):
    user = message.from_user.id
    try: 
        await nora.kick_chat_member(message.chat.id, user) 
        await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    await message.reply("As your wish!")

@nora.on_message(cmd("dban") & filters.group)
@adminsOnly
@selfadmin
async def dban(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
      return
    msg = message.reply_to_message
    if not msg:
       await message.reply("Reply to a msg to delete it and ban the user!")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await msg.delete()
        await nora.kick_chat_member(message.chat.id, msg.from_user.id) 
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(msg.from_user.id)
    await message.reply("Succesfully Banned {} in {}".format(info.mention, message.chat.title))

@nora.on_message(cmd("sban") & filters.group)
@adminsOnly
@selfadmin
async def dban(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
      return
    msg = message.reply_to_message
    if not msg:
       await message.reply("Reply to a msg to delete your msg and ban the user!")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await message.delete()
        await nora.kick_chat_member(message.chat.id, msg.from_user.id) 
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(msg.from_user.id)
    await message.reply("Succesfully Banned {} in {}".format(info.mention, message.chat.title))


@nora.on_message(cmd("dkick") & filters.group)
@adminsOnly
@selfadmin
async def dban(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
      return
    msg = message.reply_to_message
    if not msg:
       await message.reply("Reply to a msg to delete it and ban the user!")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await msg.delete()
        await nora.kick_chat_member(message.chat.id, msg.from_user.id) 
        await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(msg.from_user.id)
    await message.reply("Succesfully Kicked {} in {}".format(info.mention, message.chat.title))

@nora.on_message(cmd("skick") & filters.group)
@adminsOnly
@selfadmin
async def dban(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
      return
    msg = message.reply_to_message
    if not msg:
       await message.reply("Reply to a msg to delete it and ban the user!")
       return
    if admind_res:
       await message.reply("Dumb, You can't restrict a admin!")
       return
    try:
        await message.delete()
        await nora.kick_chat_member(message.chat.id, msg.from_user.id) 
        await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    info = await nora.get_users(msg.from_user.id)
    await message.reply("Succesfully Kicked {} in {}".format(info.mention, message.chat.title))

