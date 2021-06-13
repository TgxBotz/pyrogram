import requests
from pyrogram import filters
from pyrogram.types import (
 InlineKeyboardButton,
 InlineKeyboardMarkup,
 InputTextMessageContent,
 InlineQueryResultArticle,
 InlineQueryResultPhoto
)
from SpamBot.helpers.admins import selfadmin

from .. import *
import os
from tpblite import TPB

invalid = [
   "xnxx.com",
   "pornhub.com",
   "brattysis.com",
   "brazzers.com",
   "wtfpass.com",
   "sex.com",
   "xvideos.com"
]

@nora.on_message(cmd("webshot"))
async def webshot(client, message):
    try:
      xx = await message.reply("`Processing.......`")
      try:
          input = message.text.split(" ", 1)[1]
      except IndexError:
          await xx.edit("Give a url")
      if input in invalid:
         await xx.edit("Purn Sites Not Supported!")
         return
      try:
         await nora.send_photo(
           message.chat.id,
           f"https://webshot.amanoteam.com/print?q={input}"
         )
         await xx.delete()
      except TypeError:
          await xx.edit("Invalid Url")
      await xx.delete()
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`") 
    

@nora.on_inline_query(filters.regex("webshot"))
async def web(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a url",
           description="You haven't given any url for getting it's webshot.",
           input_message_content=InputTextMessageContent("*Webshot Gen**\nYou haven't given me any url to get its webshot.."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="webshot ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    url = f"https://shot.screenshotapi.net/screenshot?url={input}"
    try:
        requests.get(url)
    except requests.ConnectionError:
        kk = [(InlineQueryResultArticle(
         title="Invalid Url",
         description=" Provided URL is Invalid",
         input_message_content=InputTextMessageContent("**Webshot Gen**\nProvided Url is invalid"),
         reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="webshot ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=kk)
        return
    hm = requests.get(url).json()
    ss = hm.get("screenshot")
    dn = [(InlineQueryResultPhoto(
     title="Succesfully Generated WebShot",
     description="Succesfully Generated WebShot of url",
     caption=f"Successfully Generated WebShot of {input}",
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="webshot ")]
     ])
     ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)
       

@nora.on_inline_query(filters.regex("torrent"))
async def torent(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a word to get its ud results.",
           description="You haven't given any word for getting it's ud results.",
           input_message_content=InputTextMessageContent("**Uʙ Dɪᴄᴛɪᴏɴᴀʀʏ**\nYou haven't given me any word to get its info.."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="ud ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return

    results = []
    hn = TPB()
    query = hn.search(input)
    for torrent in query:
        name = torrent.title
        seeds = torrent.seeds
        leech = torrent.leeches
        size = torrent.filesize
        magnet = torrent.magnetlink
        text = f"""
**Tᴏʀʀᴇɴᴛ Sᴇᴀʀᴄʜ -** `{input}`

**Nᴀᴍᴇ -** `{name}`
**Sᴇᴇᴅᴇʀs -** `{seeds}`
**Lᴇᴇᴄʜᴇʀs -** `{leech}`
**FɪʟᴇSɪᴢᴇ -** `{size}`
**Mᴀɢɴᴇᴛɪᴄ-Lɪɴᴋ -** `{magnet}`
"""
        results.append(
          InlineQueryResultArticle(
             title=f"{name}",
             description=f"Seeders: {seeds}\nLeechers: {leech}\nFile-Size: {size}",
             input_message_content=InputTextMessageContent(text),
             thumb_url="https://telegra.ph/file/e6a881fb608296f4721f4.jpg")
        )        
    await client.answer_inline_query(iq.id, cache_time=0, results=results)
