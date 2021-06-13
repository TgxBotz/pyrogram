from .. import *
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
from pyrogram import filters
import random

@nora.on_inline_query(filters.regex("gay"))
async def gay(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a users Username/ID",
           description="You haven't given any user's Username or ID",
           input_message_content=InputTextMessageContent("**Gᴀʏ Dᴇᴛᴇᴄᴛᴏʀ**\nType a users username to detect it's Gayness!"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="gay ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
    user = await client.get_users(input)
    uname = user.username
    gey = random.randint(0, 99)
    text = f"""
**Gᴀʏ Dᴇᴛᴇᴄᴛᴏʀ -** `@{uname}`

**User -** `@{uname}`
**Gᴀʏɴᴇss -** `{gey}%`
"""
    dn = [(InlineQueryResultArticle(
      title=f"User {uname} is {gey}% Gay 🏳️‍🌈",
      description=f"Detected Gayness of {uname}",
      input_message_content=InputTextMessageContent(text),
      reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="gay"), 
      InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"gay {input}")]
      ])
    ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)
