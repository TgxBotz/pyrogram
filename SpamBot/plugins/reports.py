""" Reporting Module! """

from .. import nora, cmd
import asyncio


async def admins(message):
    admin = []
    for user in nora.iter_chat_members(
            message.chat.id, filter="administrators"
            ):
    admin.append(user.user.username)
    return admin

@nora.on_message(cmd("report"))
async def reporting(_, message):
    if message.reply_to_message:
        admins = await admins(message)
        kk = f"@{admin}\n"
        msg = await message.reply(
                kk
        )
        await kk.edit(
                "Report The Message to admins!"
        )
        return
    await message.reply(
       "Reply to a message to report it!"
    )
