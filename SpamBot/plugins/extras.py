from SpamBot import *
from telethon import events, Button
from datetime import timedelta
import os
import requests
from telegraph import Telegraph, upload_file, exceptions


@nora.on_message(cmd("paste"))
async def paste(client, message):
    if message.reply_to_message:
      msg = message.reply_to_message.text
    elif not message.reply_to_message and len(message.command) != 1:
      msg = message.text.split(" ", 1)[1]
    elif not message.reply_to_message and len(message.command) == 1:
      await message.reply("Reply to some msg or give a msg to paste it to nekobin!")
      return
    file = await message.reply_to_message.download()
    m_list = open(file, "r").read()
    message_s = m_list
    os.remove(file)

    key = (
        requests.post("https://nekobin.com/api/documents", json={"content": message_s})
        .json()
        .get("result")
        .get("key")
    )
    url = f"https://nekobin.com/{key}"
    raw = f"https://nekobin.com/raw/{key}"
    reply_text = f"**NekoBin:** {url}\n**Raw:** {raw}"
    await pablo.edit(reply_text)


@nora.on_message(cmd("telegraph"))
async def telegraph(client, message):
    xx = await message.reply("`Processing.........`")
    if not message.reply_to_message:
      await xx.edit("Reply to a image to get its Telegraph Link")
      return
    if not message.reply_to_message.media:
       await xx.edit("Reply to image not anything else......")
       return
    
    url = await message.reply_to_message.download()
    try:
       dn = upload_file(url)
    except BaseException as be:
       await xx.edit(f"**Error:**\n`{be}`")
       return
    os.remove(url)
    await xx.edit(
     f"Uploaded your pic to Telegraph\nhttps://telegra.ph/{dn[0]}",
     disable_web_page_preview=False
    )
