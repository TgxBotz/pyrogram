import requests
from SpamBot import *
from pyrogram import filters
import random
from pyrogram.types import (
   InlineKeyboardButton,
   InlineKeyboardMarkup,
   InputTextMessageContent,
   InlineQueryResultArticle,
   InlineQueryResultPhoto
)
from tinydb import TinyDB, Query
from random import choice
import string
from tpblite import TPB
import json

wdb = TinyDB("SpamBot/helpers/secret.json")

@nora.on_message(cmd("ud"))
async def ud(client, message):
    xx = await message.reply("`Searching.......`")
    input = message.command[1]
    if not input:
       await xx.edit("Please provide something to search.")
       return
    url = requests.get(f'https://api.urbandictionary.com/v0/define?term={input}')
    res = url.json()
    kk = res.get('list')
    if not kk:
       await xx.edit("No Results Found.")
       return
    definition = res['list'][0]['definition']
    example = res['list'][0]['example']
    await xx.edit(f"`{definition[:493]}`\n\n**Examples:**\n__{example}__")

@nora.on_inline_query(filters.regex("ud"))
async def hehe(client, iq):
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
    url = requests.get(f'https://api.urbandictionary.com/v0/define?term={input}')
    res = url.json()
    kk = res.get('list')
    if not kk:
        failed = [(InlineQueryResultArticle(
         title="No Results Found",
         description="No Results Found according to your search",
         input_message_content=InputTextMessageContent("**Uʙ Dɪᴄᴛɪᴏɴᴀʀʏ**\nNo Results Found according to your search"),
         reply_markup=InlineKeyboardMarkup([
         [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="ud ")]
         ])
        ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=failed)

    definition = res['list'][0]['definition']
    example = res['list'][0]['example']
    dn = []
    text = f"""
**☞ Uʀʙᴀɴ Dɪᴄᴛɪᴏɴᴀʀʏ:**

`{definition[:493]}`

**Examples:**
__{example}__
"""
    dn.append(InlineQueryResultArticle(
      title=f"{input} Results",
      description=f"Results of {input}\nExample: {example}",
      input_message_content=InputTextMessageContent(text),
      thumb_url="https://telegra.ph/file/de1183171bbb8256b8b0e.jpg",
      reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="ud ")],
      [InlineKeyboardButton("Sʜᴀʀᴇ Iᴛ", switch_inline_query=f"ud {input}")]
      ])
    ))
    await client.answer_inline_query(iq.id, cache_time=0, results=dn) 

@nora.on_message(cmd("repo"))
async def repo(client, message):
    buttons = [
       [InlineKeyboardButton("GɪᴛHᴜʙ Rᴇᴘᴏ", url="https://GitHub.com/TgxBotz/TelethonGPbot"), InlineKeyboardButton("Hᴇʀᴏᴋᴜ Dᴇᴘʟᴏʏ", url="https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FTgxBotz%2FTelethonGPBot&template=https%3A%2F%2Fgithub.com%2FTgxBotz%2FTelethonGPBot%2Fblob%2Fmain")],
       [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Cʜᴀᴛ", url="https://t.me/TgxSupportChat")]
       ]
    text = """
<b>Tɢx Rᴇᴘᴏ</b>

<b>Rᴇᴘᴏ -</b> https://github.com/TgxBotz/TelethonGPBot
<b>Uᴘᴅᴀᴛᴇs -</b> @TgxBots
<b>Sᴜᴘᴘᴏʀᴛ -</b> @TheTelegramChats
"""
    msg = message.reply_to_message
    if not msg:
      await message.reply(
       text, 
       parse_mode="HTML",
       disable_web_page_preview=True,
       reply_markup=InlineKeyboardMarkup(buttons)
      )
      return

    await client.send_message(
     message.chat.id, 
     text, 
     disable_web_page_preview=False, 
     parse_mode="HTML", 
     reply_markup=InlineKeyboardMarkup(buttons)
    )

@nora.on_message(cmd("gay"))
async def gay(client, message):
    if message.reply_to_message.from_user.id == 1704673514:
       await message.reply("Bhootnike tu hai gay, mera owner nahi!")
       return
    msg = message.reply_to_message
    ga = random.randint(0, 99)
    if not msg:
       await message.reply(f"You are {ga}% gay🏳️‍🌈")
       return
    await msg.reply("{} is {}% gay 🏳️‍🌈".format(msg.from_user.mention, ga))

@nora.on_inline_query(filters.regex("whisper"))
async def wspr(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
        user, msg = input.split("|")
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a user's id/Username",
           description="You haven't given any user's id/Username",
           input_message_content=InputTextMessageContent("**Whisper**\nGive a user's id/Username to send him a whisper.\n\n**Example:** `@NoraFatehiBot whisper @username|This is a private msg!`"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇnd Aɢᴀɪɴ", switch_inline_query_current_chat="whisper ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    except ValueError:
        eh = [(InlineQueryResultArticle(
         title="Please Give a msg too",
         input_message_content=InputTextMessageContent("Whisper\nYou haven't given any msg for whisper"),
         reply_markup=InlineKeyboardMarkup([
         [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="whisper ")]
         ])
        ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=eh)
        return
    try:
       ui = await nora.get_users(user)
    except BaseException as be:
     user_e = [(InlineQueryResultArticle(
      title="Invalid User's ID/Username",
      input_message_content=InputTextMessageContent("**Whisper**\nInvalid User id/Username"),
      reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="whisper ")]
      ])
     ))] 
     await client.answer_inline_query(iq.id, cache_time=0, results=user_e)
     return
    chars = string.hexdigits
    randomc = "".join(choice(chars) for _ in range(4))
    stark_data = {"secret_code": randomc, "id": ui.id, "msg": msg}
    wdb.insert(stark_data)
    text = f"""
A Whisper Has Been sent
to {ui.mention}!
Click The Below Button
to see message!
**Note:** __Only {ui.first_name} can
see this msg!__
"""

    dn = [(InlineQueryResultArticle(
     title=f"A Whisper To {ui.first_name}",
     description="A Secret Msg!!!",
     input_message_content=InputTextMessageContent(text),
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Show Message!", callback_data=f"sm_{randomc}")]
     ])
     ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)

@nora.on_callback_query(filters.regex("sm_(.*)"))
async def showms(client, cb):
    data = cb.matches[0].group(1)
    moment = Query()
    ms = wdb.search(moment.secret_code == data)
    if ms == []:
       await cb.answer("Oops!\nIts Looks like msg got deleted", show_alert=True)
       return

    dev = [1704673514]
    ids = ms[0]["id"]
    dev.append(int(ids))
    if cb.from_user.id not in dev:
       await cb.answer("This msg isn't for you nibba", show_alert=True)
       return

    await cb.answer(ms[0]["msg"], show_alert=True)

@nora.on_inline_query(filters.regex("pypi"))
async def pypi(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = (
         InlineQueryResultArticle(
           title="Give a name to search",
           description="You haven't given anything to Search",
           input_message_content=InputTextMessageContent("**PʏPɪ Sᴇᴀʀᴄʜ**\nGive a name to search!"),
           reply_markup=InlineKeyboardMarkup([
           [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="pypi ")]
           ])
        ))
        await client.answer_inline_query(iq.id, cache_time=0, results=[lund])
        

    url = f'https://pypi.org/pypi/{input}/json'
    try:
       res = requests.get(url).json()
    except json.decoder.JSONDecodeError:
       await client.answer_inline_query(
        iq.id, 
        cache_time=0,
        results=[],
        switch_pm_text="No module found.....",
        switch_pm_parameter="start"
       )
       return

    kk = res.get("info")
    author = kk.get("author")
    name = kk.get("name")
    license = kk.get("license")
    homee = kk.get("project_urls")
    home = homee.get("Homepage") 
    des = kk.get("summary")
    pro = kk.get("project_url")
    ver = kk.get("version")
    hogaya = []
    text = f"""
**PʏPɪ Sᴇᴀʀᴄʜ:**
**Nᴀᴍᴇ -** `{name}`
**Aᴜᴛʜᴏʀ -** `{author}`
**Lᴀᴛᴇsᴛ Vᴇʀsɪᴏɴ -** `{ver}`
**Lɪᴄᴇɴsᴇ -** `{license}`
**GɪᴛHᴜʙ Lɪɴᴋ -** `{home}`
**Dᴇsᴄʀɪᴘᴛɪᴏɴ -** `{des}`
"""
    hogaya.append(
     InlineQueryResultArticle(
        title=f"{name}",
        description=f"{des}",
        thumb_url="https://telegra.ph//file/ba2a51600d61685dbdf47.jpg",
        input_message_content=InputTextMessageContent(text),
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="pypi "),
        InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"pypi {input}")],
        [InlineKeyboardButton("Lɪɴᴋ", url=f"{pro}")]
        ])
      ))
    await client.answer_inline_query(iq.id, cache_time=0, results=hogaya)

@nora.on_inline_query(filters.regex("bin"))
async def bin(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = (
         InlineQueryResultArticle(
           title="Give a bin to check",
           description="Give a bin to check.",
           input_message_content=InputTextMessageContent("**Bɪɴ-Cʜᴇᴄᴋᴇʀ**\nGive a bin to check it."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="bin ")]
            ])
        ))
        await client.answer_inline_query(iq.id, cache_time=0, results=[lund])
        

    url = requests.get(f"https://bins-su-api.now.sh/api/{input}")
    res = url.json()
    data = res.get("data")
    textn = f"""
**❎ Invalid Bin:**
**Bin:** __{input}__
**Status:** __Invalid__
"""
    if not data:
        invalid = [(InlineQueryResultArticle(
         title="Invalid Bin",
         description="This bin is invalid",
         thumb_url="https://telegra.ph//file/21967e31b2af889e0932f.jpg",
         input_message_content=InputTextMessageContent(textn),
         reply_markup=InlineKeyboardMarkup([
         [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="bin ")]
         ])
         ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=invalid)
    else:

        vendor = data.get('vendor')
        type = data.get('type')
        level = data.get('level')
        bank = data.get('bank')
        country = data.get('bank')
        valid = f"""
**✅ Valid Bin:**
**Bin:** __{input}__
**Vendor:** __{vendor}__
**Level:** __{level}__
**Bank:** __{bank}__
**Country:** __{country}__
"""
        dn = [(InlineQueryResultArticle(
         title="Valid Bin",
         description="It's a valid bin",
         thumb_url="https://telegra.ph//file/6fc2c4615fc7a1e452adc.jpg",
         input_message_content=InputTextMessageContent(valid),
         reply_markup=InlineKeyboardMarkup([
          [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="bin "),
          InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"bin {input}")],
          ])
         ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)

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
     photo_url=f"{ss}",
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
    await client.answer_inline_query(
      iq.id, 
      cache_time=0, 
      results=results,
      switch_pm_text=f"Showing {len(results)} Results",
      switch_pm_parameter="start"
    )
