from pyrogram import filters
from SpamBot import *
from SpamBot.helpers.admins import adminsOnly, selfadmin
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

PINS_TEXT = """
**✘ All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!**

‣ `?pin` - To pinned a reply msg.
‣ `?unpin` - To Unpin the latest pinned msg.
‣ `?unpinall` - To unpinall all pinned msgs at once.
‣ `?pinned` - To get current pinned msg.

**➥Note:** __Add `notify` after ?pin to notify all chat members.__
"""

@nora.on_message(cmd("pin"))
@adminsOnly
@selfadmin
async def pin(perm, message):
    if not perm.can_pin_messages:
       await message.reply("You don't have enough rights to use this cmd:CanPinMsgs")
       return
    
    if not message.reply_to_message:
        await message.reply("Reply to a msg a msg to pin it")
        return
    try:
        await nora.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    chat_id = (str(message.chat.id)).replace("-100", "")
    msg_id = message.reply_to_message.message_id
    await message.reply(f"Succesfully Pinned [this](t.me/c/{chat_id}/{msg_id}) message.")

@nora.on_message(cmd("unpin"))
@adminsOnly
@selfadmin
async def pin(perm, message):
    if not perm.can_pin_messages:
       await message.reply("You don't have enough rights to use this cmd:CanPinMsgs")
       return
    if not message.reply_to_message:
        await message.reply("Reply to a msg to unpin it")
        return
    try:
        await nora.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    chat_id = (str(message.chat.id)).replace("-100", "")
    msg_id = message.reply_to_message.message_id
    await message.reply(f"Successfully Unpinned [this](t.me/c/{chat_id}/{msg_id}) message.")     
 
@nora.on_message(cmd("permapin"))
@adminsOnly
@selfadmin
async def pin(perm, message):
    if not perm.can_pin_messages:
       await message.reply("You don't have enough rights to use this cmd:CanPinMsgs")
       return
    
    if message.reply_to_message and not len(message.command) != 1:
        msgg = message.reply_to_message.text
    elif not message.reply_to_message and len(message.command) != 1:
        msgg = message.text.split(None, 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
        await message.reply("Reply to a msg or give a msg to pin it")
    try:
        dn = await nora.send_message(message.chat.id, msgg)
        await nora.pin_chat_message(message.chat.id, dn.message_id)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")

@nora.on_message(cmd("unpinall"))
@adminsOnly
@selfadmin
async def unpinall(perm, message):
    if not perm.can_pin_messages:
       await message.reply("You don't have enough rights to use this cmd:CanPinMsgs")
       return
    text = """
Are you sure you wanna 
unpinall all msgs at 
once!
**Note:** __This action can't be undone!__
"""
    btn = InlineKeyboardMarkup([
     [InlineKeyboardButton("Unpinall Msgs", callback_data="unpin")],
     [InlineKeyboardButton("Cancel", callback_data="cancel")]
     ]
    )
    await nora.send_message(
        message.chat.id,
        text=text,
        reply_markup=btn
    )


@nora.on_callback_query(filters.regex("unpin"))
async def unpinall_call(message, callback_query):
    user = await nora.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    if not user.status in ("creator"):
       await callback_query.answer("Group Creator Required!")
       return
    await nora.unpin_all_chat_messages(callback_query.message.chat.id)
    await callback_query.edit_message_text("Succesfully Unpinned all msgs")


@nora.on_callback_query(filters.regex("cancel"))
async def unpinall_call(message, callback_query):
    user = await nora.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    if not user.status in ("creator"):
       await callback_query.answer("Group Creator Required!")
       return
    
    await callback_query.edit_message_text("Succesfully Cancelled Unpinall cmd!")


@nora.on_callback_query(filters.regex("pins"))
async def _(client, callback_query):
    await callback_query.answer()
    await callback_query.edit_message_text(PINS_TEXT, reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
       ]
      )
    )
