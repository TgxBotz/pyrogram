from SpamBot.helpers.mongo import (
        add_sudo, rm_sudo, already_sudo,
        gban_user, ungban_user, already_gbanned,
        get_all_sudos
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


@nora.on_message(cmd("gban"))
async def gban_(client, message):
    sudos = await already_sudo(message.from_user.id)
    if message.from_user.id != sudos or message.from_user.id != DEB:
        await message.reply(
                "You cant use this cmd!"
        )
        return
                
    if len(message.command) == 1:
        await message.reply("Reply to a user or give its id to gban him!")

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    await gban_user(user_id)
    if len(message.command) == 2:
        reason = message.text.split(None, 2)[1]
    else:
        reason = "No Reason!"
    try:
        get_user = await nora.get_users(user_id)
    except BaseException as be:
        await message.reply("**Error:**\n`{be}`")
        return

    await nora.send_message(
            LOG_CHAT, 
            MSG.format(
                get_user.mention,
                message.from_user.nention,
                g_id,
                reason 
            )

    )

    await message.reply(
            "Succesfully Gbanned {}".format(
                get_user.mention
                )
            )


            
