from telethon import events, Button
from SpamBot import *
from SpamBot.helpers.admins import adminsOnly, selfadmin
from pyrogram.types import ChatPermissions

@nora.on_message(cmd("mute"))
@selfadmin
@adminsOnly
async def mute(perm, message):
    if not perm.can_restrict_members:
         await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
         return
    if message.reply_to_message:
       user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
       user = message.text.split(None, 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
       await message.reply(
        "Give a user's id or username or reply to his msg to mute him!"
       )
       return
    users = await nora.get_users(user)
    try:
       await nora.restrict_chat_member(message.chat.id, user, ChatPermissions())
    except BaseException as be:
       await message.reply(f"**Error:**\n`{be}`")
       return
    await message.reply(
     f"Succesfully Muted {users.mention}"
    )

@nora.on_message(cmd("unmute"))
@selfadmin
@adminsOnly
async def mute(perm, message):
    if not perm.can_restrict_members:
         await message.reply("You are missing the following rights to use this cmd:CanBanUsers")
         return
    if message.reply_to_message:
       user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
       user = message.text.split(None, 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
       await message.reply(
        "Give a user's id or username or reply to his msg to unmute him!"
       )
       return
    users = await nora.get_users(user)
    try:
       await nora.unban_chat_member(message.chat.id, user)
    except BaseException as be:
       await message.reply(f"**Error:**\n`{be}`")
       return
    await message.reply(
     f"Succesfully Unmuted {users.mention}"
    )
