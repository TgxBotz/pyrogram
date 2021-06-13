from .. import *
from telethon import events, Button
from GoogleNews import GoogleNews
from telethon.tl.types import InputWebDocument
import requests
from pyrogram import filters
from pyrogram.types import (
   InlineKeyboardMarkup,
   InlineKeyboardButton,
   InputTextMessageContent,
   InlineQueryResultArticle
)


@nora.on_inline_query(filters.regex("news"))
async def news(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a word to get its news results.",
           description="You haven't given any word for getting it's news results.",
           input_message_content=InputTextMessageContent("**Nᴇᴡs**\nYou haven't given me any word to get its info.."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="news ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    results = []
    url = f"https://newsapi.org/v2/everything?q={input}&from=2021-04-22&sortBy=publishedAt&apiKey=5afdc3d7f6854e5cbc2866c2e9694a09"
    res = requests.get(url).json()
    hn = res["articles"]
    for kk in hn:
        title = kk["source"]["name"]
        desc = kk["description"]
        link = kk["url"]
        img = kk["urlToImage"]
        date = kk["publishedAt"]
        text = f"""
**Nᴇᴡs -** `{input}`

**Tɪᴛʟᴇ -** `{title}`
**Pᴏsᴛᴇᴅ -** `{date}`

**Dᴇsᴄʀɪᴘᴛɪᴏɴ -** `{desc}`
"""
        results.append(InlineQueryResultArticle(
          title=f"{title}",
          description=f"{desc}",
          thumb_url="https://telegra.ph/file/f72a9ebbd3b740728cbd6.jpg",
          input_message_content=InputTextMessageContent(text),
          reply_markup=InlineKeyboardMarkup([
          [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="news"),
          InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"news {input}")],
          [InlineKeyboardButton("Nᴇᴡs Lɪɴᴋ", url=link)],
          ])
        ))
    await client.answer_inline_query(iq.id, cache_time=0, results=results)




















