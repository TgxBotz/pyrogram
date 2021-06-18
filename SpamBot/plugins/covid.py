from .. import *
from covid import Covid
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    InputTextMessageContent,
    InlineQueryResultArticle
)
from re import findall
from search_engine_parser import GoogleSearch
from tswift import Song

@nora.on_inline_query(filters.regex("covid"))
async def vivid(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a country name",
           description="You haven't given any country name to search.....",
           input_message_content=InputTextMessageContent("**Cᴏᴠɪᴅ Sᴇᴀʀᴄʜ:**\nGive a country name to get its covid status"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="covid ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    covid = Covid() 
    try:
        cases = covid.get_status_by_country_name((input).lower())
    except ValueError:
     fail = [(InlineQueryResultArticle(
       title="Invalid Country Name",
       description="Given Contry name is invalid",
       input_message_content=InputTextMessageContent("**Cᴏᴠɪᴅ Sᴇᴀʀᴄʜ:**\nGiven country name is invalid - __{input.capitalize()}__"),
       reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="covid ")]
               ])
           ))]
     await client.answer_inline_query(iq.id, cache_time=0, results=fail)
     return
    act = cases["active"]
    conf = cases["confirmed"]
    dec = cases["deaths"]
    rec = cases["recovered"]
    text = f"""
**{input.capitalize()}:**

**☞Cᴏᴜɴᴛʀʏ -** __{input.capitalize()}__
**☞Aᴄᴛɪᴠᴇ -** __{act}__
**☞Dᴇᴀᴛʜs -** __{dec}__
**☞Cᴏɴғɪʀᴍᴇᴅ -** __{conf}__
"""
    dn = [(InlineQueryResultArticle(
     title=f"{input} Covid Status",
     description=f'Current Covid status of {input}',
     input_message_content=InputTextMessageContent(text),
     thumb_url="https://telegra.ph/file/f3f40a70e5f9447597959.jpg",
     reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="covid "),
        InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"covid {input}")],
        ])
      ))]
    await client.answer_inline_query(iq.id, cache_time=0, results=dn)

@nora.on_inline_query(filters.regex("lyrics"))
async def lyrics(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a song name",
           description="You haven't given any song name to search.....",
           input_message_content=InputTextMessageContent("**Lʏʀɪᴄs Sᴇᴀʀᴄʜ**\nGive a song name to get its lyrics"),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="lyrics ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return
    song = Song.find_song(input)
    try:
       lyrics = song.lyrics
    except AttributeError:
     fail = [(InlineQueryResultArtice(
      title="Invalid Song Name",
      description="Song name is invalid",
      input_message_content=InputTextMessageContent(f"**Lʏʀɪᴄs Sᴇᴀʀᴄʜ:** __{input}__\nInvalid Song Name"),
      reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="lyrics ")]
               ])
           ))]
     await client.answer_inline_query(iq.id, cache_time=0, results=fail)
     return


    result = lyrics.format()
    ok = []
    ok.append(InlineQueryResultArticle(
     title=f"{song.title}",
     description=f"Song: {song.title}\nArtist: {song.artist}",
     input_message_content=InputTextMessageContent(f"**Lʏʀɪᴄs Sᴇᴀʀᴄʜ: `{input}`**\n\n**Song-Name:** __{song.title}__\n**Artist:** __{song.artist}__\n**Lyrics:** __{result}__"),
     thumb_url="https://telegra.ph/file/666e3e32a150efe7d925f.jpg",
     reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="lyrics "),
        InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"lyrics {input}")],
        ])
      ))
    await client.answer_inline_query(iq.id, cache_time=0, results=ok)

@nora.on_inline_query(filters.regex("gg"))
async def gg(client, iq):
    try:
        input = iq.query.split(" ", maxsplit=1)[1]
    except IndexError:
        lund = [(
         InlineQueryResultArticle(
           title="Give a query to search it",
           description="You haven't given any query to search.....",
           input_message_content=InputTextMessageContent("**Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ**\nGive some query to search it."),
           reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="gg ")]
               ])
           ))]
        await client.answer_inline_query(iq.id, cache_time=0, results=lund)
        return

    searcher = []
    page = findall(r"page=\d+", input)
    cache = False
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(input), int(page), bool(cache))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
            yems = "https://telegra.ph/file/f943fc0d377a4e6057d4f.jpg"
            searcher.append(
              InlineQueryResultArticle(
               title=f"{title}",
               description=desc,
               thumb_url="https://telegra.ph/file/f943fc0d377a4e6057d4f.jpg",
               input_message_content=InputTextMessageContent(f"**Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ:** __{input}__\n\n**Title:** __{title}__\n**Description:** __{desc}__"),
               reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", switch_inline_query_current_chat="gg "),
        InlineKeyboardButton("Sʜᴀʀᴇ", switch_inline_query=f"gg {input}")],
        [InlineKeyboardButton("Gᴏᴏɢʟᴇ Lɪɴᴋ", url=link)]
        ])
      ))
        except IndexError:
            break
    await client.answer_inline_query(iq.id, cache_time=0, results=searcher)
