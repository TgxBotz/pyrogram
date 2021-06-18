import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

from .. import *

p_help = InlineKeyboardMarkup([
    [InlineKeyboardButton("✘ Aᴅᴍɪɴ ✘", callback_data="admin"), InlineKeyboardButton("✘ Bᴀɴs ✘", callback_data="bans")],
    [InlineKeyboardButton("✘ Pɪɴs ✘", callback_data="pins"), InlineKeyboardButton("✘ Pᴜʀɢᴇs ✘", callback_data="purges")],
    [InlineKeyboardButton("✘ Lᴏᴄᴋs ✘", callback_data="locks"), InlineKeyboardButton("✘ Mɪsᴄ ✘", callback_data="misc")],
    [InlineKeyboardButton("✘ Tɢx Mᴏᴅᴜʟᴇs ✘", callback_data="mod"), InlineKeyboardButton("✘ NɪɢʜᴛMᴏᴅᴇ ✘", callback_data="ng")],
    [InlineKeyboardButton("✘ Aɴᴛɪ-Sᴘᴀᴍ ✘", callback_data="anti")],
    [InlineKeyboardButton("✘ GᴏIɴʟɪɴᴇ ✘", switch_inline_query_current_chat="")]
    ])


HELP_TEXT = """
**Heya @NoraFatehiBot help menu here:**

/start - To Start Me ;)
/help - To Get Available Help Menu

Report Bugs At---> **@TgxSupportChat**
All cmd can be used with !, ?, /.
"""

@nora.on_message(cmd(["help", "cmds"]))
async def help(_, message):
    if message.chat.type != "private":
       await message.reply("Contact me in PM for Quick Help", reply_markup=InlineKeyboardMarkup([
       [InlineKeyboardButton("Help And Commands ❓", url="t.me/NoraFatehiBot?start=help")]
       ]))
       return
    await message.reply(HELP_TEXT, reply_markup=p_help)


@nora.on_callback_query(filters.regex("help"))
async def help(client, cb):
    await cb.answer()
    await cb.edit_message_text(HELP_TEXT, reply_markup=p_help)


@nora.on_callback_query(filters.regex("mod"))
async def _(client, cb):
    text = """
**✘ A list of some special modules.**

‣ `?song` - To Find a song and Download it.
‣ `?github` - Find info of a GitHub User by his username.
‣ `?telegraph` - Reply to image with this cmd to get its Telegraph Link.
‣ `?paste` - To paste a text to nekobin.
‣ `?chatinfo` - Type this cmd in a group to get its whole info.
‣ `?gg` - To get Google results of any query.
‣ `?ping` - To get ping speed of bot.
‣ `?meme` - Reply to a image/sticker to create a meme.
‣ `?ud` - To get Urban Dictionary results of a query.
"""
    await cb.answer()
    await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
       ]
      )
    )
@nora.on_callback_query(filters.regex("ng"))
async def ng(client, cb):
    text = """
**✘ Do Night Spammers anoy you?
Which spams your group in night**

**‣** `?nightmode [on, off]` - To enable or disable nightmode
in your group.
"""
    await cb.answer()
    await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
     ]))
