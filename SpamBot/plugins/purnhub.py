from pornhub_api import PornhubApi
from .. import *
import carbon, asyncio
from pyrogram import filters
import io
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from google_trans_new import google_translator
import os
from datetime import datetime

P_U = [1704673514]

OWNER = [1704673514]


@nora.on_message(cmd("carbon"))
async def carbon_make(client, message):
   if message.reply_to_message:
     text = message.reply_to_message.text
   elif not message.reply_to_message and len(message.command) != 1:
     text = message.text.split(None, 1)[1]
   elif not message.reply_to_message and len(message.command) == 1:
     await message.reply("Reply to a msg to give a msg to make a carbon!")
     return
   start = datetime.now()
   xx = await message.reply("`Processing.......`")
   options = carbon.CarbonOptions(text)
   cb = carbon.Carbon()
   try:
      img = await cb.generate(options)
   except Exception as e:
      await xx.edit(f"**Erro:**\n`{e}`")
      return
   await img.save("cerbon")
   end = datetime.now()
   du = (end - start).seconds
   await client.send_document(message.chat.id, "cerbon.png", caption=f"**Generated Carbon in {du} Second(s)**")
   await xx.delete()
   os.remove(cerbon)


@nora.on_message(
        cmd("purnhub")
        & filters.user(P_U)
        & filters.private
)
async def purn(client, message):

    if len(message.command) == 1:
       await message.reply("Give something to search nigga")
       return
    api = PornhubApi()
    data = api.search.search(
    message.command[1],
    ordering="mostviewed",
    period="weekly",
    )
    results = []
    for vid in data.videos:
        title = vid.title
        du = vid.duration
        views = vid.views
        rate = vid.ratings
        url = vid.url
        text = f"""
**PᴜʀɴHᴜʙ Sᴇᴀʀᴄʜ -** `{input}`

**Tɪᴛʟᴇ -** `{title}`
**Dᴜʀᴀᴛɪᴏɴ -** `{du}`
**Vɪᴇᴡs -** `{views}`
**Rᴀᴛɪɴɢs -** `{rate}`
"""
    await message.reply(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Phub Link", url=f"{url}")]
      ]
     )
    )

@nora.on_message(cmd("tr"))
async def translate(_, message):
    if not message.reply_to_message:
       await message.reply("Reply to a msg to translate it!")
       return
    if len(message.command) == 1:
       await message.reply("Give a language code in which you wanna translate!")
       return
    translator = google_translator()
    text = translator.translate(message.reply_to_message.text, lang_tgt=message.command[1])
    await message.reply(f"**Translated:**\n`{text}`")

@nora.on_message(
   cmd("bcast")
   & filters.user(OWNER)
   & filters.private
)
async def bcast(client, message):
    text = message.text.split(" ", maxsplit=1)[1]
    ok = sql.get_all_users_id()
    for s in ok:
        try:
            await client.send_message(int(s), text)
        except:
            error += 1
            pass
    await message.reply(f"Broadcast Done With {error} Error And Sucess in {len(ok) - error}!")
