import functools
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from .. import nora, cmd

keyboard = [
   InlineKeyboardButton("Verify Me", callback_data="verify")
]

def cb_wrapper(func):
    @functools.wraps(func)
    async def callb(client, cb):
      user = cb.from_user.id
      if cb.from_user.id != user:
          await cb.answer("This Menu Wasn't Opened By You!")
      else:
          await func(client, cb)
    return callb

def anon_check(func):
    @functools.wraps(func)
    async def anon(client, message):
      if message.sender_chat:
       await message.reply(
        "It's looks like you are an Anon Admin\n__Please Click The Below Button for Verifying__",
        reply_markup=InlineKeyboardMarkup([keyboard])
       )
      else:
         await func(client, message)
    return anon

@nora.on_message(filters.regex("verify"))
async def verfy(client, cb, func, message):
    ok =  await client.get_chat_member(cb.from_user.id, cb.message.chat.id)
    if not ok in ("administrator", "creator"):
       await cb.answer("Only admins can execute this command!")
       return 
    await func(client, message)
