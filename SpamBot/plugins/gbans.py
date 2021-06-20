from SpamBot.helpers.mongo import (
        gban_user, ungban_user, already_gbanned,
)
import os
from pyrogram import filters
from .. import nora, cmd
from SpamBot.plugins.sudos import DEB

LOG_CHAT = int(os.environ.get("LOG_CHAT"))
MSG = """
**GBANNED:**

**User:** {}
**Admin:** {}
**User-ID:** `{}`
**Reason:** {}

"""

SUDOS = [1704673514]

@nora.on_message(cmd("gban"))
async def gban_(client, message):
    if message.from_user.id not in SUDOS:
        await message.reply(
                "You cant use this cmd!"
        )
        return

    if not message.reply_to_message and len(message.command) == 1:
        await message.reply("Reply to a user or give its id to gban him!")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    await gban_user(user_id)

    if len(message.command) == 2:
        reason = message.text.split(None, 2)[1]
    else:
        reason = "No Reason!"
        return
    try:
        get_user = await nora.get_users(user_id)
    except BaseException as be:
        await message.reply("**Error:**\n`{be}`")
        return
    alre = await already_gbanned(get_user.id)
    if alre:
        await message.reply(
                "He is already Gbanned!\nLoL"
        )
        return

    if get_user.id in SUDOS:
        await message.reply(
                "You cant gban a Sudo!"
        )
        return

    await nora.send_message(
            LOG_CHAT, 
            MSG.format(
                get_user.mention,
                message.from_user.mention,
                get_user.id,
                reason 
            )

    )

    await message.reply(
            "Succesfully Gbanned {}".format(
                get_user.mention
                )
            )


            
