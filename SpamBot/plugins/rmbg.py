
from SpamBot import *
import io
from datetime import datetime
import os
import requests
from SpamBot.helpers.admins import selfadmin

@nora.on_message(cmd("rmbg"))
@selfadmin
async def rmbg(client, message):
    xx = await message.reply("`Analysing......`")
    if not message.reply_to_message:
       await xx.edit("Reply to a image to remove it's background.")
       return
    dl = await client.download_media(message.reply_to_message, "./Downloads")
    if not dl.endswith(("webp", "jpg", "png", "jpeg")):
         await xx.edit("Media type not supported")
         return
    await xx.edit("`Removing Background......`")
    out = ReTrieveFile(dl)
    start = datetime.now()
    os.remove(dl)
    contentType = out.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(out.content) as remove_bg_image:
            remove_bg_image.name = "Rmbg.png"
            await client.send_document(
                message.chat.id,
                document=remove_bg_image,
                force_document=True,
                caption="Background Removed By @NoraFatehiBot!",
            )
        end = datetime.now()
        ms = (end - start).seconds
        await xx.delete()
        await message.reply(f"**Removed Background in {ms} second(s)**")
    else:
        await xx.delete()
        await message.reply("**Something went wrong**")




RMBG_API = "sVchWcxQAMRcD3LafrJzVkoB"


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": RMBG_API,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r
