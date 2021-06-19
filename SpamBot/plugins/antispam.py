""" Hemlo Unkils! """

from pyrogram import filters
from .. import arq, nora, cmd
import os
from time import time
from pyrogram.types import (
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from SpamBot.helpers.admins import adminsOnly
from SpamBot.helpers.mongo import (
        is_nsfw_on, nsfw_on, nsfw_off,
        is_flood_on, en_flood, di_flood,
        is_pdb, add_pdb, rm_pdb
)

from . import list_admins
from ProfanityDetector import detector

ANTI = """
**✘ This system can restrict
members who sends nsfw content
and spams the chat!**

**‣** `?nsfwscan [enable, disable]` - 
To Enable/Disable The Nsfw Watch in
your group!
**‣*** `?antiflood [enable, disable]` -
To Enable Flood watch in your chat!
"""
async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id

nsfw_detect_group = 1
@nora.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=nsfw_detect_group,
)
async def detection(client, message):
    if not is_nsfw_on(message.chat.id):
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await nora.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    os.remove(file)
    nsfw = results.is_nsfw
    if not nsfw:
        return
    try:
        await message.delete()
        await nora.restrict_chat_member(message.chat.id, message.from_user.id, ChatPermissions(), int(time() + 3600))
    except BaseException as be:
        await message.reply(f"**Error:** `{be}`")
        return

    text = f"""
**Detected NSFW Content:**

**User:** {message.from_user.mention}
**Porn:** `{results.porn}`
**Action:** __Muted For 1 Hour!__
"""
    await message.reply_text(
            text
    )

@nora.on_message(cmd("nsfwscan"))
@adminsOnly
async def msdw(_, message):
    is_en = await is_nsfw_on(message.chat.id)
    if len(message.command) == 1:
        await message.reply(
                f"**Current Group Nsfw Setting Is:** `{is_en}`"
        )
    inp = message.text.split(None, 1)[1]
    if inp == "enable":
        await nsfw_on(message.chat.id)
        await message.reply(
                "I have enabled Nsfw Detection System for this chat!"
        )
    elif inp == "disable":
        await nsfw_off(message.chat.id)
        await message.reply(
                "I have disabled Nsfw Detection System for this chat!"
        )
    else:
        await message.reply(
                f"Invalid Option\n**Current Setting is `{is_en}`!"
        )


DB = {}

def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0

flood_group = 2
@nora.on_message(
    ~filters.service
    & ~filters.me
    & ~filters.private
    & ~filters.channel
    & ~filters.bot
    & ~filters.edited,
    group=flood_group,
)
async def flood_detect(_, message):
    if not await is_flood_on(message.chat.id):
        return
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

    reset_flood(chat_id, user_id)

    mods = await list_admins(chat_id)
    if user_id in mods:
        return
    if DB[chat_id][user_id] >= 10:
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
**Flood Detected:**

**User:** {message.from_user.mention}
**Action:** __Muted For 1 Hour__
"""
        return await message.reply(
            text,
            reply_markup=keyboard,
        )
    DB[chat_id][user_id] += 1

@nora.on_callback_query(filters.regex("unmute_(.*)"))
async def oof(client, cb):
    user = cb.matches[0].group(1)
    ad = await nora.get_chat_member(cb.message.chat.id, cb.from_user.id)
    if ad.status not in ("administrator", "creator"):
        await cb.answer("Only admins can execute this cmd!", show_alert=True)
        return
    if not ad.can_restrict_members:
        await cb.answer("You are missing the following rights to use this cmd:CanBanUsers!", show_alert=True)
        return
    await nora.unban_chat_member(cb.message.chat.id, int(user))
    eh = await nora.get_users(int(user))
    mention = cb.from_user.mention
    text = f"""
Succesfully unmuted {eh.mention}
by {mention}
"""
    await cb.message.edit(text)


@nora.on_message(cmd("antiflood"))
@adminsOnly
async def te(_, message):
    is_en = await is_flood_on(message.chat.id)
    if len(message.command) == 1:                                                                            await message.reply(
                f"**Current Group Flood Setting Is:** `{is_en}`"                                              )
    inp = message.text.split(None, 1)[1]
    if inp == "enable":
        await en_flood(message.chat.id)
        await message.reply(
                "I have enabled Flood Detection System for this chat!"
        )
    elif inp == "disable":
        await di_flood(message.chat.id)
        await message.reply(
                "I have disabled Flood Detection System for this chat!"
        )
    else:
        await message.reply(
                f"Invalid Option\n**Current Setting is `{is_en}`!"
        )


@nora.on_message(cmd("profanity"))
@adminsOnly
async def prof(client, message):
    chat_id = message.chat.id
    is_en = await is_pdb(chat_id)
    if len(message.command) == 1:
        await message.reply(f"**Current Profanity Settings:** `{is_en}`")
        return
    ok = message.command[1]
    if ok == "enable":
        await add_pdb(chat_id)
        await message.reply("**Succesfully Enabled Profanity Detection for {}**".format(
            message.chat.title
            )
        )
    elif ok == "disable":
        await rm_pdb(chat_id)
        await message.reply("**Successfully Disabled Profanity Detection for {}".format(
            message.chat.title
            )
        )
    else:
        await message.reply("**Invalid Suffix**\n__Current Setting is {}__".format(
            is_en
            )
        )
        
prof_group = 4

@nora.on_message(
        group=prof_group
)
async def detection(client, message):
    chat_id = message.chat.id
    if not await is_pdb(chat_id):
        return
    is_admin = await nora.get_chat_member(chat_id, message.from_user.id)
    if is_admin.status in ("creator", "administrator"):
        return
    msg = message.text
    word, det = detector(msg)
    if det:
        try:
            men = message.from_user.mention
            await message.delete()
            await message.reply(f"{men} has sent a blacklisted word and I have deleted it!")
        except BaseException as be:
            await message.reply(f"**Detected a profanity word but cant delete:**\n`{be}`")


       
@nora.on_callback_query(filters.regex("anti"))
async def anti(client, cb):
    await cb.answer()
    await cb.edit_message_text(
            ANTI,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]
            ]
        )
    )



