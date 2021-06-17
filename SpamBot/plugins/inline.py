from pyrogram import filters
from pyrogram.types import (
     InlineKeyboardButton, 
     InlineKeyboardMarkup,
     InputTextMessageContent,
     InlineQueryResultArticle
)
import requests
from play_scraper import search

from SpamBot import *
from SpamBot.helpers.wrappers import cb_wrapper

ABOUT = """
<b>Bot is Alive.</b>

<b>Python:</b> <code>3.9.5</code>
<b>Pyrogram:</b> <code>1.2.9</code>
<b>Hosting:</b> <code>Heroku</code>
<b>Support:</b> @TheTelegramChats
"""

HELPN = """
<b>✘Wᴇʟᴄᴏᴍᴇ Tᴏ NᴏʀᴀFᴀᴛᴇʜɪBᴏᴛ</b>

<code>?start</code> <b>- To Start Me</b>
<code>?help</code> <b>- To Get Help Menu Of Bot</b>

<b>Updates -</b> @TgxBots
<b>Support -</b> @TgxSupportChat
"""

EX = """
<b>✘ Exᴛʀᴀs Hᴇʟᴘ Mᴇɴᴜ:</b>

<b>➤</b> <code>?github<username></code> - To get a information about a GitHub User.
<b>➤</b> <code>?telegraph</code> - Reply to a image to get it's telegraph link.
<b>➤</b> <code>?paste</code> - Reply to some text to paste it to nekobin.
<b>➤</b> <code>?chatinfo</code> - Type this in a chat to get the chatinfo.
<b>➤</b> <code>?ping</code> - To Get Ping speed of bot
<b>➤</b> <code>?gg <query></code> - To get the Google results of a query. 

<b>Updates -</b> @TgxBots
<b>Support -</b> @TgxSupportChat
"""


btn1 = [
   [InlineKeyboardButton("Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="gg "), InlineKeyboardButton("YᴏᴜTᴜʙᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="yt ")],
   [InlineKeyboardButton("GɪᴛHᴜʙ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="github "), InlineKeyboardButton("PʟᴀʏSᴛᴏʀᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="app ")],
   [InlineKeyboardButton("Lʏʀɪᴄs Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="lyrics "), InlineKeyboardButton("Cᴏᴠɪᴅ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="covid ")],
   [InlineKeyboardButton("Bɪɴ-Cʜᴇᴄᴋᴇʀ", switch_inline_query_current_chat="bin "), InlineKeyboardButton("Uʀʙᴀɴ-Dɪᴄᴛɪᴏɴᴀʀʏ", switch_inline_query_current_chat="ud ")],
   [InlineKeyboardButton("« Previous", callback_data="last"), InlineKeyboardButton("Next »", callback_data="nex")]
   ] 

btn2 = [
    [InlineKeyboardButton("PʏPɪ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="pypi "), InlineKeyboardButton("QR-Gᴇɴᴇʀᴀᴛᴏʀ", switch_inline_query_current_chat="makeqr ")],
    [InlineKeyboardButton("Rᴀɴᴅᴏᴍ-Jᴏᴋᴇ", switch_inline_query_current_chat="joke "), InlineKeyboardButton("Cᴏᴜɴᴛʀʏ-Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="country ")],
    [InlineKeyboardButton("WᴇʙSʜᴏᴛ-Gᴇɴ", switch_inline_query_current_chat="webshot "), InlineKeyboardButton("JɪᴏSᴀᴠᴀᴀɴ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="js ")],
    [InlineKeyboardButton("Tᴏʀʀᴇɴᴛ-Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="torrent "), InlineKeyboardButton("Nᴇᴡs Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="news")],
    [InlineKeyboardButton("« Previous", callback_data="inline"), InlineKeyboardButton("Next »", callback_data="last")]
    ]

btn3 = [
    [InlineKeyboardButton("Usᴇʀ-Iɴғᴏ", switch_inline_query_current_chat="whois "), InlineKeyboardButton("Sᴇɴᴅ Wʜɪsᴘᴇʀ", switch_inline_query_current_chat="whisper ")],
    [InlineKeyboardButton("Fᴀᴋᴇ Dᴀᴛᴀ-Gᴇɴ", switch_inline_query_current_chat="fakegen")],
    [InlineKeyboardButton("« Previous", callback_data="nex"), InlineKeyboardButton("Next »", callback_data="inline")]]


@nora.on_inline_query()
async def inline(client, iq):
    user = iq.from_user.id
    btn = [
    [InlineKeyboardButton("Exᴛʀᴀ-Cᴍᴅs", callback_data=f"ext_{user}"), InlineKeyboardButton("Iɴʟɪɴᴇ-Mᴇɴᴜ", callback_data=f"inline_{user}")],
    [InlineKeyboardButton("Gʀᴏᴜᴘ-Hᴇʟᴘ Cᴍᴅs", url="t.me/NoraFatehiBot?start=start")]
    ]
    if len(iq.query) != 0: 
        return 
    alive = (InlineQueryResultArticle(
     title=f"Bot Alive.",
     description="Current Bot Status",
     thumb_url="https://telegra.ph//file/f81da799a4ad11aea8d1d.jpg",
     input_message_content=InputTextMessageContent(ABOUT),
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Hᴇʟᴘ-Mᴇɴᴜ", callback_data="menu")]
     ])
    ))

    help = (InlineQueryResultArticle(
     title=f"Help Menu",
     description="Bot Help-Menu",
     thumb_url="https://telegra.ph//file/9a5d6cd3327c039d3eabd.jpg",
     input_message_content=InputTextMessageContent(HELPN),
     reply_markup=InlineKeyboardMarkup(btn)
    ))

    await client.answer_inline_query(
     iq.id, 
     cache_time=0, 
     results=[alive, help],
     switch_pm_text="Start Me in PM 👥",
     switch_pm_parameter="start"
    )
 
@nora.on_message(cmd("inline"))
async def inline(_, message):
    await message.reply(
      "**Inline Help-Menu**",
      reply_markup=InlineKeyboardMarkup(btn1)
    ) 
       
@nora.on_callback_query(filters.regex("menu_(.*)"))
async def ex(client, cb):
    btn = [
    [InlineKeyboardButton("Exᴛʀᴀ-Cᴍᴅs", callback_data=f"ext_{cb.from_user.id}"), InlineKeyboardButton("Iɴʟɪɴᴇ-Mᴇɴᴜ", callback_data=f"inline_{cb.from_user.id}")],
    [InlineKeyboardButton("Gʀᴏᴜᴘ-Hᴇʟᴘ Cᴍᴅs", url="t.me/NoraFatehiBot?start=start")]
    ]
  
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
        await cb.answer("This menu wasnt opened by you\n#Phuck_Aff", show_alert=True)          
        return
    await cb.answer()
    await cb.edit_message_text(
      HELPN,
      parse_mode="HTML",
      reply_markup=InlineKeyboardMarkup(btn)
    )

@nora.on_callback_query(filters.regex("ext_(.*)"))
async def ext(client, cb):
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
        await cb.answer("This menu wasnt opened by you\n#Phuck_Aff", show_alert=True)
        return

    await cb.answer()
    await cb.edit_message_text(
      EX,
      reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data=f"menu_{cb.from_user.id}")]
      ]))

@nora.on_callback_query(filters.regex("inline_(.*)"))
async def inline(client, cb):
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
        await cb.answer("This menu wasnt opened by you\n#Phuck_Aff", show_alert=True)          
        return
    btn1 = [
    [InlineKeyboardButton("Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="gg "), InlineKeyboardButton("YᴏᴜTᴜʙᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="yt ")],
    [InlineKeyboardButton("GɪᴛHᴜʙ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="github "), InlineKeyboardButton("PʟᴀʏSᴛᴏʀᴇ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="app ")],
    [InlineKeyboardButton("Lʏʀɪᴄs Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="lyrics "), InlineKeyboardButton("Cᴏᴠɪᴅ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="covid ")],
    [InlineKeyboardButton("Bɪɴ-Cʜᴇᴄᴋᴇʀ", switch_inline_query_current_chat="bin "), InlineKeyboardButton("Uʀʙᴀɴ-Dɪᴄᴛɪᴏɴᴀʀʏ", switch_inline_query_current_chat="ud ")],
    [InlineKeyboardButton("« Previous", callback_data=f"last_{cb.from_user.id}"), InlineKeyboardButton("Next »", callback_data=f"nex_{cb.from_user.id}")]
    ]
    await cb.answer()
    await cb.edit_message_text(
     "**Inline Help Menu:**",
     reply_markup=InlineKeyboardMarkup(btn1)
    )

@nora.on_callback_query(filters.regex("nex_(.*)"))
async def nex(client, cb):
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
        await cb.answer("This menu wasnt opened by you\n#Phuck_Aff", show_alert=True)          
        return
    btn2 = [
    [InlineKeyboardButton("PʏPɪ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="pypi "), InlineKeyboardButton("QR-Gᴇɴᴇʀᴀᴛᴏʀ", switch_inline_query_current_chat="makeqr ")],
    [InlineKeyboardButton("Rᴀɴᴅᴏᴍ-Jᴏᴋᴇ", switch_inline_query_current_chat="joke "), InlineKeyboardButton("Cᴏᴜɴᴛʀʏ-Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="country ")],
    [InlineKeyboardButton("WᴇʙSʜᴏᴛ-Gᴇɴ", switch_inline_query_current_chat="webshot "), InlineKeyboardButton("JɪᴏSᴀᴠᴀᴀɴ Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="js ")],
    [InlineKeyboardButton("Tᴏʀʀᴇɴᴛ-Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="torrent "), InlineKeyboardButton("Nᴇᴡs Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="news")],
    [InlineKeyboardButton("« Previous", callback_data=f"inline_{cb.from_user.id}"), InlineKeyboardButton("Next »", callback_data=f"last_{cb.from_user.id}")]
    ]
    await cb.answer()
    await cb.edit_message_text("**Inline Menu:**",
     reply_markup=InlineKeyboardMarkup(btn2)
    )


@nora.on_callback_query(filters.regex("last_(.*)"))
async def lasst(client, cb):
    user = int(cb.matches[0].group(1))
    if cb.from_user.id != user:
        await cb.answer("This menu wasnt opened by you\n#Phuck_Aff", show_alert=True)          
        return
     btn3 = [
     [InlineKeyboardButton("Usᴇʀ-Iɴғᴏ", switch_inline_query_current_chat="whois "), InlineKeyboardButton("Sᴇɴᴅ Wʜɪsᴘᴇʀ", switch_inline_query_current_chat="whisper ")],
     [InlineKeyboardButton("Fᴀᴋᴇ Dᴀᴛᴀ-Gᴇɴ", switch_inline_query_current_chat="fakegen")],
     [InlineKeyboardButton("« Previous", callback_data=f"nex_{cb.from_user.id}"), InlineKeyboardButton("Next »", callback_data=f"inline_{cb.from_user.id}")]
     ]
     await cb.answer()
     await cb.edit_message_text(
      "**Inline HelpMenu**",
      reply_markup=InlineKeyboardMarkup(btn3)
    )
