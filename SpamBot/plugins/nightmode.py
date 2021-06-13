from pyrogram import filters
from pyrogram.types import ChatPermissions
from SpamBot import nora, cmd
import pytz 
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from SpamBot.helpers.mongo import (
    is_night_chat_in_db, 
    get_all_night_chats, 
    rm_night_chat, 
    add_night_chat
)
from SpamBot.helpers.admins import adminsOnly, selfadmin
import logging

@nora.on_message(cmd("nightmode") & filters.group)
@adminsOnly
@selfadmin
async def night(perm, message):
    if not perm.can_change_info:
       await message.reply("You are missing the following rights to use this command:CanChangeInfo")
       return
    if len(message.command) != 2:
        await message.reply_text("Give me a value that you wanna disable or enable NightMode!")
        return
    status = message.text.split(" ", 1)[1].strip()
    stats = status.lower()
    if stats in ("on", "enable"):
      already = await is_night_chat_in_db(message.chat.id)
      if already:
        await message.reply("This chat has NightMode Enabled Already!")
        return
      await add_night_chat(message.chat.id)
      await message.reply(f"Succesfully Enabled NightMode For {message.chat.title}!")
    elif status in ("off", "disable"):
      if not already:
        await message.reply("This chat hasn't enabled NightMode!")
    else:
        await message.reply("Unknown cmd!\n__/nightmode [enable, on]__ or __/nightmode [off, disable]__")


async def job_close():
    lol = await get_all_night_chats()
    if len(lol) == 0:
        return
    for warner in lol:
        try:
            await nora.send_message(
              int(warner.get("chat_id")), "Its 12:00 Am, Group Is Closing! Group will be locked until 6 Am!\n**Powered By @NoraFatehiBot**"
            )
            await nora.set_chat_permissions(warner.get("chat_id"), ChatPermissions())
            
        except Exception as e:
            logging.info(str(e))
            ido = warner.get("chat_id")
            try:
                await nora.send_message(int(warner.get("chat_id")), f"Failed to close Group\n**Error:** `{e}`")
            except:
                pass

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()


async def job_open():
    lol = await get_all_night_chats()
    if len(lol) == 0:
        return
    for warner in lol:
        try:
            await nora.send_message(
              int(warner.get("chat_id")), "Its 06:00 Am, Group Is Opening! Group will be again locked at 12 Am!\n**Powered By @NoraFatehiBot**"
            )
            await nora.set_chat_permissions(
                        warner.get("chat_id"),
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_stickers=True,
                            can_send_animations=True
                         )
            )
        except Exception as e:
            logging.info(str(e))
            ido = warner.get("chat_id")
            try:
                await nora.send_message(int(warner.get("chat_id")), f"Failed to open Group\n**Error:** `{e}`")
            except:
                pass

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=5, minute=59)
scheduler.start()
