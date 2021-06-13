
from .. import nora
import requests
from pyrogram import filters

C_C = [-1001220406140]

"""
@nora.on_message(())
async def chatbot(_, message):
    if message.reply_to_message and message.reply_to_message.from_user.id == 1704673514:
         input = message.command
         url = f"http://api.brainshop.ai/get?bid=155827&key=tVhEcHqwrXqtCNZT&uid=73948&msg={input}"
         res = requests.get(url).json()
         ans = res.get("cnt")
         await message.reply(ans)
         return
"""
