from .. import *
import pyrogram
import os
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultPhoto
)


@nora.on_message(cmd(["info", "whois"]))
async def info(_, message):
    xx = await message.reply("`Processing.....`")
    if message.reply_to_message:
            user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
            user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
            user = message.text.split(None, 1)[1]
    pic, infor = await user_info(user)
    if not pic:
        await xx.edit(infor, parse_mode="HTML")
        return
    photo = await nora.download_media(pic)
    await nora.send_document(message.chat.id, photo, caption=infor)
    await xx.delete()
    os.remove(photo)

@nora.on_inline_query(filters.regex("whois"))
async def inlineinfo(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a user's Username or ID to get his info.",
           description="You haven't given any user's Username or ID to get his info.",
           input_message_content=InputTextMessageContent("**Usᴇʀ-Iɴғᴏ:**\nGive a user's Username or ID to get his info"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="whois ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    try:
       user = await nora.get_users(input)
    except Exception as e:
       fail = [(InlineQueryResultArticle(
        title=f"No User Found",
        description="Something Went Wrong",
        input_message_content=InputTextMessageContent(f"**Error:**\n`{e}`"),
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="whois ")]
        ])
       ))]
       await client.answer_inline_query(iq.id, cache_time=20, results=fail)
       return

    first = user.first_name if user.first_name else "Deleted Account"
    last = user.last_name if user.last_name else "No Last Name Found"
    uname = user.username if user.username else "No Username Found"
    id = user.id
    dc = user.dc_id if user.dc_id else None
    stats = user.status
    bot = user.is_bot
    scam = user.is_scam
    ver = user.is_verified
    link = user.mention
    
    user_msg = f"""
**Exᴛʀᴀᴄᴛᴇᴅ UsᴇʀIɴғᴏ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ Dᴀᴛᴀʙᴀsᴇ**

**➥ ID:** `{id}`
**➥ Dᴄ-ID:** `{dc}`
**➥ FɪʀsᴛNᴀᴍᴇ:** {first}
**➥ LᴀsᴛNᴀᴍᴇ:** {last}
**➥ Usᴇʀɴᴀᴍᴇ:** {uname}
**➥ Sᴛᴀᴛᴜs:** __{stats}__
**➥ Is Bᴏᴛ:** __{bot}__
**➥ Sᴄᴀᴍ:** __{scam}__
**➥ Vᴇʀɪғɪᴇᴅ:** __{ver}__
**➥ Pᴇʀᴍᴀʟɪɴᴋ:** {link}
"""
    dn = [(InlineQueryResultArticle(
     title=f"{first}",
     description=f"Name: {first}\nID: {id}\nUsername: {uname}",
     input_message_content=InputTextMessageContent(user_msg),
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="whois "),
     InlineKeyboardButton("Share Info", switch_inline_query=f"whois {input}")],
     [InlineKeyboardButton("User-Link", url=f"tg://user?id={id}")]
     ])
    ))]
    await client.answer_inline_query(iq.id, cache_time=20, results=dn)
    

async def user_info(user):
    try:
       user = await nora.get_users(user)
    except BaseException as be:
       fail = f"""
**Error:**
`{be}`
"""
       return fail 

    user_id = user.id
    first = user.first_name
    last = user.last_name
    uname = user.username
    status = user.status
    mention = user.mention
    dc_id = user.dc_id
    photo = user.photo.big_file_id if user.photo else None

    capt = f"""
<b>Exᴛʀᴀᴄᴛᴇᴅ UsᴇʀIɴғᴏ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ Dᴀᴛᴀʙᴀsᴇ</b>

<b>➥ ID :</b> <code>{user_id}</code>
<b>➥ Dᴄ-ID :</b> <code>{dc_id}</code>
<b>➥ FɪʀsᴛNᴀᴍᴇ :</b> {first}
<b>➥ LᴀsᴛNᴀᴍᴇ :</b> {last}
<b>➥ Usᴇʀɴᴀᴍᴇ :</b> @{uname}
<b>➥ Sᴛᴀᴛᴜs :</b> <code>{status}</code>
<b>➥ Is Bᴏᴛ :</b> <code>{user.is_bot}</code>
<b>➥ Sᴄᴀᴍ :</b> <code>{user.is_scam}</code>
<b>➥ Vᴇʀɪғɪᴇᴅ :</b> <code>{user.is_verified}</code>
<b>➥ Pᴇʀᴍᴀʟɪɴᴋ :</b> {mention}
"""
    return [photo, capt]

@nora.on_message(cmd("chatinfo"))
async def xinfo(_, message):
    xx = await message.reply("`Processing.......`")
    if len(message.command) != 1:
      chat = message.text.split(None, 1)[1]
    elif not len(message.command) != 1:
      chat = message.chat.id
    try:
       pic, info = await chat_info(chat)
    except BaseException as be:
       await xx.edit(f"**Error:**\n`{be}`")
       return
    if not pic:
        await xx.edit(info, parse_mode="HTML")
        return
    photo = await nora.download_media(pic)
    await xx.delete()
    await nora.send_document(
      message.chat.id,
      photo,
      caption=info
      )
    os.remove(photo)

async def chat_info(chat):
    try:
       chat = await nora.get_chat(chat)
    except BaseException as be:
       fail = f"""
**Error:**
`{be}`
"""
       return fail 
    title = chat.title
    chat_id = chat.id
    type = chat.type
    uname = chat.username
    scam = chat.is_scam
    restricted = chat.is_restricted
    count = chat.members_count
    dc_id = chat.dc_id
    desc = chat.description
    photo = chat.photo.big_file_id if chat.photo else None
    link = f"[link](t.me/{uname})" if uname else None

    capt = f"""
<b>Chatinfo:</b>

<b>Tɪᴛʟᴇ :</b> <code>{title}</code>
<b>ID :</b> <code>{chat_id}</code>
<b>Dᴄ-ID :</b> <code>{dc_id}</code>
<b>Tʏᴘᴇ :</b> <code>{type}</code>
<b>Usᴇʀɴᴀᴍᴇ :</b> <code>{uname}</code>
<b>Pᴀʀᴛɪᴄɪᴘᴀɴᴛɪɴᴛs :</b> <code>{count}</code>
<b>Sᴄᴀᴍ :</b> <code>{scam}</code>
<b>Rᴇsᴛʀɪᴄᴛᴇᴅ :</b> <code>{restricted}</code>
<b>CʜᴀᴛLɪɴᴋ :</b> {link}

<b>Dᴇsᴄʀɪᴘᴛɪᴏɴ :</b>
<code>{desc}</code>
"""
    return [photo, capt]
