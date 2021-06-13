import os
import heroku3
import requests
from SpamBot import *
import time


@nora.on_message(cmd("logs"))
async def _(_, message):
    if message.from_user.id != 1704673514:
      await message.reply("You don't have acces to use this cmd.")
      return
    k = await message.reply("`Scrapping logs.....`")
    Heroku = heroku3.from_key("3310bee9-b46d-4414-9e63-c68cc5098be6")
    app = Heroku.app("fuckdynos")
    ok = app.get_log()
    url = "https://del.dog/documents"
    r = requests.post(url, data=ok.encode("UTF-8")).json()
    logs = f"https://del.dog/{r['key']}"
    await k.edit("Sent app logs in your private chat.")
    await nora.send_message(
       1704673514, 
       f"**Logs:** {logs}"
    )

