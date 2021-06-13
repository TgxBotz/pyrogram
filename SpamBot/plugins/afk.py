from .. import *
from SpamBot.plugins.sql import afk_sql as sql
from pyrogram import filters
import random

"""
options = [
                "{} is here!",
                "{} is back!",
                "{} is now in the chat!",
                "{} is awake!",
                "{} is back online!",
                "{} is finally here!",
                "Welcome back! {}",
                "Where is {}?\nIn the chat!",
                "Pro {}, is back alive!",
            ]
nub = random.choice(options)

@nora.on_message(filters.command(r"(.*?)"))
async def afk(event):
    sender = message.from_user.id
    if event.text.startswith("/afk"):
     cmd = event.text[len("/afk ") :]
     if cmd is not None:
        reason = cmd
     else:
        reason = ""
     fname = sender.first_name   
     start_time = fname
     sql.set_afk(sender.id, reason, start_time)
     await event.reply(
           "{} is now AFK!".format(fname),
           parse_mode="markdown")
     return
    if event.text.startswith("Brb"):
     cmd = event.text[len("Brb ") :]
     if cmd is not None:
        reason = cmd
     else:
        reason = ""
     fname = sender.first_name
     start_time = fname
     sql.set_afk(sender.id, reason, start_time)
     await event.reply(
           "{} is now AFK!".format(fname),
           parse_mode="markdown")
     return
    if event.text.startswith("brb"):
     cmd = event.text[len("brb ") :]
     if cmd is not None:
        reason = cmd
     else:
        reason = ""
     fname = sender.first_name
     start_time = fname
     sql.set_afk(sender.id, reason, start_time)
     await event.reply(
           "{} is now AFK!".format(fname),
           parse_mode="markdown")
     return

    if sql.is_afk(sender.id):
       res = sql.rm_afk(sender.id)
       if res:
          firstname = sender.first_name
          loda = nub.format(firstname)
          await event.reply(loda, parse_mode="markdown")


@tgxbot.on(events.NewMessage())
async def _(event):
    msg = await event.get_reply_message()
    if msg:
       if sql.is_afk(msg.sender_id):  
          user = sql.check_afk_status(msg.sender_id)
          if not user.reason:             
              await event.reply("{} is AFK!".format(user.start_time))
          else:        
              await event.reply("{} is AFK!\n**Reason:** `{}`".format(user.start_time, user.reason))
"""
