import glitchart
from SpamBot import nora, cmd
from pyrogram import types 
import os

@nora.on_message(cmd("glitch"))
async def glitch(_, message):
    try:
       xx = await message.reply("`Processing.......`")
       if not message.reply_to_message:
          await xx.edit("Please reply to something to glitch it.")
          return
       if not message.reply_to_message.media:
          await xx.edit("Please reply to a valid media to glitch it.")
          return
       file = await nora.download_media(message.reply_to_message)
       pic = glitchart.mp4(file) 
       await nora.send_animation(
        message.chat.id,
        pic
       )
       
       await xx.delete()
    except BaseException as be:
      await message.reply(f"**Error:**\n`{be}`")
    os.remove(file)
