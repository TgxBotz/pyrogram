""" Hemlo Unkils! """

from pyrogram import filters
from .. import arq, nora, cmd
import os
from time import time
from pyrogram.types import ChatPermissions
from SpamBot.helpers.admins import adminsOnly
from SpamBot.helpers.mongo import is_nsfw_on, nsfw_on, nsfw_off

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
    inp = message.text.split(None, 1)[1].strip().lower()
    if ("enable", "on") in inp:
        await nsfw_on(message.chat.id)
        await message.reply(
                "I have enabled Nsfw Detection System for this chat!"
        )
    elif ("disable", "off") in inp:
        await nsfw_off(message.chat.id)
        await message.reply(
                "I have disabled Nsfw Detection System for this chat!"
        )
    else:
        await message.reply(
                f"Invalid Option\n**Current Setting is `{is_en}`!"
        )
