import requests
from pyrogram import filters
from SpamBot import *
import time
from re import findall
import pybase64
import json
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
import os

@nora.on_message(cmd("github"))
async def github(client, message):
    k = await message.reply("`Processing.......`")
    try:
       input_str = message.command[1]
    except IndexError:
        await k.edit("Give a Github user's Username to get its info")
        return  
    url = f"https://api.github.com/users/{input_str}"
    re = requests.get(url)
    if re.status_code == 404: 
        await k.edit("No User Found According to your search.")
        return

    kk = re.json()
    avatar_url = kk["avatar_url"]
    html_url = kk["html_url"]
    gh_type = kk["type"]
    name = kk["name"]
    company = kk["company"]
    blog = kk["blog"]
    location = kk["location"]
    bio = kk["bio"]
    created_at = kk["created_at"]

    caption = f"""
<b>✘ GɪᴛHᴜʙ Sᴇᴀʀᴄʜ:</b>

<b>Nᴀᴍᴇ -</b> <code>{name}</code>
<b>Tʏᴘᴇ -</b> <code>{gh_type}</code>
<b>Lᴏᴄᴀᴛɪᴏɴ -<b> <code>{location}</code>
<b>Cᴏᴍᴘᴀɴʏ -</b> <code>{company}</code>
<b>Bʟᴏɢ -</b> <code>{blog}</code>
<b>Lɪɴᴋ -</b> <code>{html_url}</code>

<b>Bɪᴏ -</b> <code>{bio}</code>
"""

    time.sleep(1)
    await k.delete()
    await client.send_document(
        message.chat.id,
        document=avatar_url,
        file_name=f"{name}",
        caption=caption,
        parse_mode="HTML")

@nora.on_inline_query(filters.regex("github"))
async def callback_git(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a GitHub user's Username",
           description="You haven't given any github user's Username to get his info.",
           input_message_content=InputTextMessageContent("**GɪᴛHᴜʙ Sᴇᴀʀᴄʜ:**\nGive a GitHub user's Username to get his info"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="github ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    url = f"https://api.github.com/users/{input}"
    re = requests.get(url)
    if re.status_code == 404: 
      fail = [(InlineQueryResultArticle(
        title="No User Found",
        description="No Results Found",
        input_message_content=InputTextMessageContent("**GɪᴛHᴜʙ Sᴇᴀʀᴄʜ:**\nInvalid Username"),
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="github ")]
        ])
      ))]
      await client.answer_inline_query(iq.id, cache_time=0, results=fail)
      return
    kk = re.json()
    avatar_url = kk["avatar_url"]
    html_url = kk["html_url"]
    gh_type = kk["type"]
    name = kk["name"]
    company = kk["company"]
    blog = kk["blog"]
    location = kk["location"]
    bio = kk["bio"]
    created_at = kk["created_at"]
    follow = kk["followers"]
    uname = kk["login"]
    repo = kk["public_repos"]
    caption = f"""
<b>✘ GɪᴛHᴜʙ Sᴇᴀʀᴄʜ:</b>

<b>➤Nᴀᴍᴇ -</b> <code>{name}</code>
<b>➤Usᴇʀɴᴀᴍᴇ -</b> <code>{uname}</b>
<b>➤Tʏᴘᴇ -</b> <code>{gh_type}</code>
<b>➤Lᴏᴄᴀᴛɪᴏɴ -<b> <code>{location}</code>
<b>➤Cᴏᴍᴘᴀɴʏ -</b> <code>{company}</code>
<b>➤Bʟᴏɢ -</b> <code>{blog}</code>
<b>➤Rᴇᴘᴏs -</b> <code>{repo}</code>
<b>➤Fᴏʟʟᴏᴡᴇʀs -</b> <code>{follow}</code>

<b>➤Bɪᴏ -</b> <code>{bio}</code>
""" 
    dn = [(InlineQueryResultPhoto(
      photo_url=f"{html_url}",
      caption=caption,
      parse_mode="HTML",
      title=f"{name} GitHub",
      description=f"GitHub Info of {name}",
      reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="github "),
        InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"github {input}")],
        [InlineKeyboardButton("GɪᴛHᴜʙ Lɪɴᴋ", url=f"{html_url}")]
        ])
      ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)
