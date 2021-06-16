import functools
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from .. import nora, cmd


def cb_wrapper(func):
    @functools.wraps(func)
    async def callb(client, cb):
      user = cb.from_user.id
      if cb.from_user.id != user:
          await cb.answer("This Menu Wasn't Opened By You!")
      else:
          await func(client, cb)
    return callb

def anon_check(**args):
    @functools.wraps(func)
    async def anon(client, message):
        perm = args.get("perm")
        keyboard = [
          InlineKeyboardButton("Verify Me", callback_data=f"verify_{perm}")
        ]
  
        text = """
It looks like you are an
anon admin!
__Please Click The Below Button
"""        
        if message.sender_chat:
            await message.reply(text, reply_markup=InlineKeyboardMarkup(
                [keybaord]
            )
        else:
            await func(client, message)
    return anon


@nora.on_message(filters.regex("verify_(.*)"))
async def verify(client, cb):
     perm = cb.matches[0].group(1)
     ok = await client.get_chat_member(cb.message.chat.id, cb.from_user.id)
     if not ok in ("admininstrator", "creator"):
         await cb.answer(
             "Only admins can execute this command!",
             show_alert=True
         )
     elif not perms:
         await cb.answer(
             "You are missing the following rights to use this command:{perms}",
             show_alert=True
        )

     else:
         pass
         
