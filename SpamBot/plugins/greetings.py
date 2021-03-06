from SpamBot import nora
from pyrogram import filters
from datetime import timedelta
import random
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ChatPermissions
)

MSGS = [
  "Will meet you soon",
  "Someone left us alone",
  "Someone has left the game"
] 

WLC_TEXT = """
<b>Hi</b> <b><a href="tg://user?id={}">{}</a></b>
Welcome to {}!
Here you can do Masti/Spam/Etc.
<b>Read</b> <b><a href="t.me/NoraFatehiBot?start=Rules">Rules</a> to avoid bans and dont spam!</b>
<b>Click the below button for unmuting yourself!</b>
"""

user = {}

@nora.on_message(filters.new_chat_members)
async def welcome(client, message):
    await client.restrict_chat_member(message.chat.id, message.from_user.id, ChatPermissions(can_send_messages=False))
    await message.reply(
    WLC_TEXT.format(
      message.from_user.id,
      message.from_user.first_name,
      message.chat.title,
    ),
    parse_mode="HTML",
    disable_web_page_preview=True,
    reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton("Click Here To Unmute", callback_data="welcome")]
    ]))
    user.update({"user": message.from_user.id})
 
@nora.on_callback_query(filters.regex("welcome"))
async def welcome_mute(client, cb):
    user_s = user["user"]
    if cb.from_user.id != user_s:
        await cb.answer("This captcha isn't for you!", show_alert=True)
        return
    await nora.unban_chat_member(message.chat.id, user_s)
