from SpamBot import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

RULES = """
**Rules**:

➥Dont Do Offtopic
➥No Promotions
➥No Abusing
➥Dont Tag Admins Without Reasons
➥No Selling
➥Dont Delete Your Messages
➥Try to use English As It's A International Chat
"""

@nora.on_message(cmd("rules"))
async def rules(client, message):

    await client.send_message(
     message.chat.id,
     "Contact me in PM to get chat rules",
     reply_markup=InlineKeyboardMarkup([
     [InlineKeyboardButton("Chat Rules", url="https://t.me/NoraFatehiBot?start=rules")]
     ])
    )
