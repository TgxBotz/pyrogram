""" Reporting Module! """

from .. import nora, cmd
import asyncio


async def admins(chat_id: int):
    admin = []
    async for user in nora.iter_chat_members(
            chat_id, filter="administrators"
            ):
           admin.append(user.user.username)
    return admin

@nora.on_message(cmd("report"))
async def reporting(_, message):
    if message.reply_to_message:
        async for user in nora.iter_chat_members(
            message.chat.id, filter="administrators"
            ):
            ad = user.user.username
      
        kk = f"@{ad}\n"
        msg = await message.reply(
                kk)
        await msg.edit(
                "Report The Message to admins!"
          )
        return
    await message.reply(
       "Reply to a message to report it!"
    )
