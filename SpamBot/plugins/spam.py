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

def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0


@nora.on_message(
        ~filters.service
        & ~filters.me
        & ~filters.private
        & ~filters.channel
)
async def flood(client, message: Message):
    chat_id = message.chat.id

    # Initialize db if not already.
    if chat_id not in DB:
        DB[chat_id] = {}

    if not message.from_user:
        reset_flood(chat_id)
        return

    user_id = message.from_user.id
    mention = message.from_user.mention

    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    # Reset floodb of current chat if some other user sends a message
    reset_flood(chat_id, user_id)

    # Ignore devs and admins
    mods = (await list_admins(chat_id)) + DEVS
    if user_id in mods:
        return

    # Mute if user sends more than 7 messages in a row
    if DB[chat_id][user_id] >= 7:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=int(time() + 3600),
            )
        except Exception:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" Unmute ",
                        callback_data=f"unmute_{user_id}",
                    )
                ]
            ]
        )
        text = f"""
**⚠️ Spam-Detection ⚠️**

**User:** {mention}
**Chat:** `{chat_id}`

__Muted {mention} for 1 hour
as he tried to spam the chat!__
"""
        return await message.reply_text(
            text,
            reply_markup=keyboard,
        )
    DB[chat_id][user_id] += 1

