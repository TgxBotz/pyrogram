from youtubesearchpython import VideosSearch
from .. import nora, cmd
from pyrogram import filters
from pyrogram.types import (
  InlineKeyboardButton, 
  InlineKeyboardMarkup,
  InputTextMessageContent,
  InlineQueryResultArticle,
  InlineQueryResultPhoto
)

import requests
import os

@nora.on_message(cmd("yt"))
async def yt_message(_, message):
    await message.reply("`@NoraFatehiBot yt`")

@nora.on_inline_query(filters.regex("yt"))
async def yt(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a word to get its results.",
           description="You haven't given any word for getting it's results.",
           input_message_content=InputTextMessageContent("**Yt Search**\nYou haven't given me any word to get its yt results.."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="yt ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return

    results = []
    search = VideosSearch(input, limit=20)
    res = search.result()
    result = res["result"]
    for k in result:
        title = k["title"]
        link = k["link"]
        du = k["duration"]
        id = k["id"]
        vi = k["viewCount"]
        views = vi["text"]
        chan = k["channel"]
        channel = chan["name"]
        th = k["thumbnails"]
        img = th[0]["url"]
        pic = f"https://img.youtube.com/vi/{id}/hqdefault.jpg"
        text = f"""
**YᴏᴜTᴜʙᴇ Sᴇᴀʀᴄʜ:**
**Tɪᴛʟᴇ -** `{title}`
**Cʜᴀɴɴᴇʟ -** `{channel}`
**Vɪᴇᴡs -** `{views}`
**Dᴜʀᴀᴛɪᴏɴ -** `{du}`
"""  
        results.append( 
          InlineQueryResultPhoto(
             photo_url=pic,
             title=f"{title}",
             description=f"Channel: {channel}\nViews: {views}\nDuration: {du}",
             caption=text,
             reply_markup=InlineKeyboardMarkup([
             [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="yt "), 
             InlineKeyboardButton("Sʜᴀʀᴇ Iᴛ", switch_inline_query=f"yt {input}")],
             [InlineKeyboardButton("YᴏᴜTᴜʙᴇ Uʀʟ", url=f"{link}")]
             ])))
    await client.answer_inline_query(
     iq.id, 
     cache_time=0, 
     results=results,
     switch_pm_text=f"Showing {len(results)} Results",
     switch_pm_parameter="start"
    )


@nora.on_inline_query(filters.regex("js"))
async def js(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a word to get its results.",
           description="You haven't given any word for getting it's results.",
           input_message_content=InputTextMessageContent("**JioSavaan Search**\nYou haven't given me any word to get its js results.."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="yt ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return

    url = f"http://starkmusic.herokuapp.com/result/?query={input}"
    res = requests.get(url).json()
    results = []
    for kk in res:
        name = kk["music"]
        album = kk["album"]
        singer = kk["singers"]
        du = kk["duration"]
        link = kk["perma_url"]
        dl_url = kk["media_url"]
        text = f"""
**JɪᴏSᴀᴠᴀᴀɴ Sᴇᴀʀᴄʜ -** `{input}`
**Nᴀᴍᴇ -** `{name}`
**Sɪɴɢᴇʀ -** `{singer}`
**Aʟʙᴜᴍ -** `{album}`
**Dᴜʀᴀᴛɪᴏɴ -** `{du}`
**Lɪɴᴋ -** `{link}`
"""
        results.append(
          InlineQueryResultArticle(
              title=f"Song - {name}",
              description=f"Song - {name}\nSinger - {singer}\nDuration - {du}",
              thumb_url="https://telegra.ph//file/2b9918123d152f5e46339.jpg",
              input_message_content=InputTextMessageContent(text),
              reply_markup=InlineKeyboardMarkup([
             [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="js "), 
             InlineKeyboardButton("Sʜᴀʀᴇ Iᴛ", switch_inline_query=f"js {input}")],
             [InlineKeyboardButton("JɪᴏSᴀᴠᴀᴀɴ Uʀʟ", url=f"{link}")]
             ])))

    await client.answer_inline_query(
     iq.id, 
     cache_time=0, 
     results=results,
     switch_pm_text=f"Showing {len(results)} Results",
     switch_pm_parameter="start"
    )
