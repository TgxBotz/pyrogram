from .. import *
from pyrogram import filters
from pyrogram.types import (
   InlineKeyboardButton,
   InlineQueryResultArticle,
   InlineKeyboardMarkup,
   InputTextMessageContent,
   InlineQueryResultPhoto
)
import requests
import os
from play_scraper import search

@nora.on_inline_query(filters.regex("makeqr"))
async def makeqr(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give some text to make a Qr of it.",
           description="You haven't given any text to make QR",
           input_message_content=InputTextMessageContent("**Qʀ Gᴇɴᴇʀᴀᴛᴏʀ**\nGive some text to make a qr of it."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="makeqr ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    url = f'https://api.qrserver.com/v1/create-qr-code/?data={input}'
    res = requests.get(url)
    file = "NoraFatehi.png"
    with open(file, "w+b") as k:
      for chunk in res.iter_content(chunk_size=128):
        k.write(chunk)
   
    dn = [(InlineQueryResultPhoto(
     title="Created QR Code",
     description=f"Created QR Code Of {input}",
     photo_url=file,
     caption=f"Succesfully Created QR code by @NoraFatehiBot\n__User /scanqr in my PM reply to this msg to decode it :)__",
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Mᴀᴋᴇ Aɢᴀɪɴ", switch_inline_query_current_chat="makeqr ")],
     [InlineKeyboardButton("Sʜᴀʀᴇ Iᴛ", switch_inline_query=f"makeqr {input}")]
     ])
    ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)

@nora.on_inline_query(filters.regex("joke"))
async def joke(client, iq):
    url = "https://official-joke-api.appspot.com/random_joke"
    res = requests.get(url).json()
    joke = res.get("setup")
    punch = res.get("punchline")
    dn = [(InlineQueryResultArticle(
     title="Rᴀɴᴅᴏᴍ Jᴏᴋᴇ",
     description=f"Joke: {joke}\nPunchLine: {punch}",
     input_message_content=InputTextMessageContent(f"**Rᴀɴᴅᴏᴍ Jᴏᴋᴇ**\n\n**Joke:** __{joke}__\n**Punchline:** __{punch}__"),
     thumb_url="https://telegra.ph/file/0b6bebd9f43f903f5223a.jpg",
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="joke ")]
     ])
     ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)

@nora.on_inline_query(filters.regex("country"))
async def country(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a country name to get its info.",
           description="You haven't given any country name for getting its info.",
           input_message_content=InputTextMessageContent("**Cᴏᴜɴᴛʀʏ Sᴇᴀʀᴄʜ**\nGive a country name to get its info."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="country ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    url = f"https://restcountries.eu/rest/v2/name/{input}?fullText=true"
    res = requests.get(url).json()
    try:
       name = res[0]["name"]
    except KeyError:
       fail = [(
         InlineQueryResultArticle(
           title="Give a valid country name to get its info.",
           description="You haven't given any valid country name for getting its info.",
           input_message_content=InputTextMessageContent("**Cᴏᴜɴᴛʀʏ Sᴇᴀʀᴄʜ**\nGive a valid country name to get its info."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="country ")]
               ])
           ))]
       await client.answer_inline_query(iq.id, cache_time=0, results=fail)
       return
    cap = res[0]["capital"]
    region = res[0]["region"]
    pop = res[0]["population"]
    img = res[0]["flag"]
    text = f"""
**{name.capitalize()} Cᴏᴜɴᴛʀʏ Iɴғᴏ:**
**Nᴀᴍᴇ -** `{name}`
**Cᴀᴘɪᴛᴀʟ -** `{cap}`
**Pᴏᴘᴜʟᴀᴛɪᴏɴ -** `{pop}`
**Rᴇɢɪᴏɴ -** `{region}`
"""
    dn = [(InlineQueryResultArticle(
     title=f"{name} Cᴏᴜɴᴛʀʏ Iɴғᴏ",
     description=f"Country Info Of {name}",
     thumb_url=f"{img}",
     input_message_content=InputTextMessageContent(text),
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="country ")],
     [InlineKeyboardButton("Sʜᴀʀᴇ Iᴛ", switch_inline_query=f"country {input}")]
     ])
     ))]
    await client.answer_inline_query(iq.id, results=dn)

