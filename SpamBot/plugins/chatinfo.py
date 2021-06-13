from .. import *
import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
import os

@nora.on_message(cmd("getpic"))
async def bots(client, message):
    k = await message.reply("`Getting picture....`")
    msg = message.reply_to_message
    if not msg:
       await k.edit("`Reply to a file.....`")
       return
    if not msg.document:
       await k.edit("`Reply to a file not anything else....`")
       return
    a = await client.download_media(msg, "./Downloads")
    s = open(a, "r")
    c = s.read()
    s.close()
    pygments.highlight(
        f"{c}",
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "pic.png",
    )
    await client.send_document(
        message.chat.id, "pic.png"
    )
    await k.delete()
    os.remove(a)
    os.remove("pic.png")


