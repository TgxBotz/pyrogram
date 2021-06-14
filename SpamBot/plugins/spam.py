from .. import nora, cmd
from pyrogram import filters
from time import time
from pyrogram.types import (
   InlineKeyboardMarkup, 
   InlineKeyboardButton,
   ChatPermissions,
   Message,
   CallbackQuery
)

async def list_admins(chat_id: int):
    list_of_admins = []
    async for member in nora.iter_chat_members(
        chat_id, filter="administrators"
    ):
        list_of_admins.append(member.user.id)
    return list_of_admins

DB = {}
DEVS = [1704673514, 1157157702] 

@nora.on_message(
        ~filters.service
        & ~filters.me
        & ~filters.private
        & ~filters.channel
)
async def flood(client, message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    mention = message.from_user.mention
    chat_id = message.chat.id

    mods = (await list_admins(chat_id)) + DEVS
    if user_id in mods:
        return

    if chat_id not in DB:
        DB[chat_id] = {}
    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0
    
    if DB[chat_id][user_id] >= 10:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=int(time() + 3600)
                    )
        except Exception:
            return
    text = f"""
**⚠️ Spam-Detection ⚠️**

**User:** {mention}
**Chat:** `{chat_id}`

__Muted {mention} for 1 hour
as he tried to spam the chat!__
"""
    keyboard = [
     InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup([keyboard]))

    DB[chat_id][user_id] += 1

    
