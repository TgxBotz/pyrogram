from SpamBot import *
from SpamBot.helpers.admins import adminsOnly

OT = """
It looks like you are doing offtopic here!
This chat is for On-Topic chat. Please move to @TheTelegramChats
"""

@nora.on_message(cmd("ot"))
@adminsOnly
async def ot(client, message):
    await message.delete()
    await nora.send_message(
     message.chat.id, 
     OT
    )

    text = """
**User {} [wrote](t.me/c/{}/{}):**

`{}`

⬇️ Please Continue Here ⬇️
""".format(
     message.reply_to_message.from_user.mention if message.reply_to_message else None,
     message.chat.id,
     message.reply_to_message.message_id if message.reply_to_message else None,
     message.reply_to_message.text if message.reply_to_message else None
    )

    await nora.send_message(
     "TheTelegramChats",
     text
    )
