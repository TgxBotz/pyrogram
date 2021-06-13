from pyrogram import filters
from SpamBot import *
from SpamBot.helpers.admins import adminsOnly, selfadmin
import time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


PR_HELP = """
**✘ Need to delete lots of messages? That's what purges are for!**

‣ `?purge` - Reply to a msg to delete msgs from there.
‣ `?spurge` - Same as purge, but doesnt send the final confirmation message.
‣ `?del` - Deletes the replied to message.
"""

@nora.on_message(cmd("purge"))
@selfadmin
@adminsOnly
async def purge(perm, message):
    if not perm.can_delete_messages:
      await message.reply("You are missing the following rights to use this command:CanDeleteMessages")
      return
    chat_id = message.chat.id
    message_ids = []
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To A Message To Let Me Know Where To Start Purging From!"
        )
    await message.delete()
    for a_s_message_id in range(
        message.reply_to_message.message_id, message.message_id
    ):
        message_ids.append(a_s_message_id)
        if len(message_ids) == 100:
            await nora.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    try:
       if len(message_ids) > 0:
        await nora.delete_messages(
            chat_id=chat_id, message_ids=message_ids, revoke=True
       )
       await message.reply("Purged!")
    except Exception as e:
       await message.reply("**Error:**\n`{e}`")


@nora.on_message(cmd("spurge"))
@selfadmin
@adminsOnly
async def purge(perm, message):
    if not perm.can_delete_messages:
      await message.reply("You are missing the following rights to use this command:CanDeleteMessages")
      return
    chat_id = message.chat.id
    message_ids = []
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To A Message To Let Me Know Where To Start Purging From!"
        )
    await message.delete()
    for a_s_message_id in range(
        message.reply_to_message.message_id, message.message_id
    ):
        message_ids.append(a_s_message_id)
        if len(message_ids) == 100:
            await nora.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    try:
       if len(message_ids) > 0:
        await nora.delete_messages(
            chat_id=chat_id, message_ids=message_ids, revoke=True
       )
    except Exception as e:
       await message.reply("**Error:**\n`{e}`")

    
@nora.on_message(cmd("del"))
@selfadmin
@adminsOnly
async def delmsg(perm, message):
    if not perm.can_delete_messages:
      await message.reply("You are missing the following rights to use this command:CanDeleteMessages")
      return
    if not message.reply_to_message:
      await message.reply("Reply to a msg to delete it!")
      return
    try:
       await message.reply_to_message.delete()
       await message.delete()
    except Exception as e:
       await message.reply("**Error:**\n`{e}`")

@nora.on_callback_query(filters.regex("purges"))
async def purges(client, cb):
    await cb.answer()
    await cb.edit_message_text(PR_HELP, reply_markup=InlineKeyboardMarkup([
         [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
        ]
      )
    )
