from SpamBot.helpers.mongo import (
        add_sudo, rm_sudo, already_sudo
)
from pyrogram import filters
import os
LOG_CHAT = int(os.environ.get("LOG_CHAT"))

ADD_MSG = """
**New Sudo:**

**User:** {}
**By:** @TheStarkXD
"""

from SpamBot import nora, cmd
DEB = 1704673514

@nora.on_message(cmd("addsudo"))
async def adding_sumdo(client, message):
    if message.from_user.id != DEB:
        await message.reply(
                "Only Dev Can use this comnand!"
        )
        return
    if len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        await message.reply(
                "Reply to a user or give its id to add sudo!"
        )
        return
    alre = await already_sudo(user_id)
    if alre:
     await message.reply("He is already a sudo user!")
     return
    await add_sudo(user_id)
    await nora.send_message(
            LOG_CHAT, 
            ADD_MSG
    )
    await message.reply("Promoted To Sudo!")


@nora.on_message(cmd("rmsudo"))
async def adding_sumdo(client, message):
    if message.from_user.id != DEB:
        await message.reply(
                "Only Dev Can use this comnand!"
        )
        return
    if len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        await message.reply(
                "Reply to a user or give its id to remove sudo!"
        )
        return
    await rm_sudo(user_id)
    await nora.send_message(
            LOG_CHAT,
            RM_MSG
    )
    await message.reply("Demoted from Sudo!")
