from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SpamBot import *
import os
from SpamBot.helpers.admins import adminsOnly, selfadmin
from SpamBot.helpers.wrappers import anon_check
from pyrogram import filters

@nora.on_callback_query(filters.regex("admin"))
async def _(client, callback_query):
   await callback_query.answer()
   await callback_query.edit_message_text(ADMIN_TEXT, reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton('« Bᴀᴄᴋ', callback_data="help")]
       ]
      )
    )

@nora.on_message(cmd("pinned") & filters.group)
async def pinned(client, message):
    chat = (str(message.chat.id)).replace("-100", "")
    ok = (await client.get_chat(message.chat.id)).pinned_message
    msg_id = ok.message_id
    text = f"The Pinned Message In {message.chat.title} is <a href=t.me/c/{chat}/{msg_id}>here</a>"
    await message.reply(text, parse_mode="HTML")

@nora.on_message(cmd("adminlist") & filters.group)
@selfadmin
async def adminlist(_, message):
    text = f"**Admins in {message.chat.title}:**\n\n"
    async for admins in nora.iter_chat_members(message.chat.id, filter="administrators"):
       text += f"**-** @{admins.user.username}\n"
    await message.reply(text)
 
@nora.on_message(cmd("bots") & filters.group)
@selfadmin
async def botlist(_, message):
    text = f"**Bots in {message.chat.title}:**\n\n"
    async for admins in nora.iter_chat_members(message.chat.id, filter="bots"):
       text += f"**-** @{admins.user.username}\n"
    await message.reply(text)

@nora.on_message(cmd("setgpic") & filters.group)
@anon_check(perm="can_change_info")
@selfadmin
@adminsOnly
async def setgpic(perm, message):
    if not perm.can_change_info:
       await message.reply("You don't have enough rights to use this cmd:CanChangeInfo")
       return
    msg = message.reply_to_message
    if not msg:
       await message.reply("Reply to a image to set it as group pic")
       return
    if not msg.photo:
        await message.reply("Please to a image not anything else")
        return
    pic = await nora.download_media(msg)
    try:
        await nora.set_chat_photo(message.chat.id, photo=pic)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
    await message.reply("Succesfully setted group pic")
    os.remove(pic)

@nora.on_message(cmd("promote") & filters.group)
@adminsOnly
@selfadmin
async def promote(perm, message):
    if not perm.can_promote_members:
       await message.reply("You don't have enough rights to use this cmd:CanAddAdmins")
       return
    if message.chat.type == "private":
       await message.reply("This cmd is made to be used in Groups not PM")
       return
    chat_id = message.chat.id
    BOT_ID = 1813724543
    bot = await nora.get_chat_member(chat_id, BOT_ID)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    elif not message.reply_to_message and not len(message.command) != 1:
        await message.reply("Reply to someone or give his Username or id to promote him!")

    await nora.promote_chat_member(
       chat_id, 
       user_id,
       can_manage_chat=True,
       can_change_info=True,
       can_delete_messages=True,
       can_restrict_members=False,
       can_invite_users=True,
       can_pin_messages=True,
       can_promote_members=False,
       can_manage_voice_chats=True
    )
    await message.reply("Promoted!")


@nora.on_message(cmd("demote") & filters.group)
@adminsOnly
@selfadmin
async def promote(perm, message):
    if not perm.can_promote_members:
       await message.reply("You don't have enough rights to use this cmd:CanAddAdmins")
       return
    chat_id = message.chat.id
    BOT_ID = 1813724543
    bot = await nora.get_chat_member(chat_id, BOT_ID)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    elif not message.reply_to_message and not len(message.command) != 1:
        await message.reply("Reply to someone or give his Username or id to Demote him!")

    await nora.promote_chat_member(
       chat_id, 
       user_id,
       can_manage_chat=None,
       can_change_info=None,
       can_delete_messages=None,
       can_restrict_members=None,
       can_invite_users=None,
       can_pin_messages=None,
       can_promote_members=None,
       can_manage_voice_chats=None
    )
    await message.reply("Demoted!")


@nora.on_message(cmd(["chatlink", "invitelink"]) & filters.group)
@adminsOnly
@selfadmin
async def invitelink(perm, message):
    if not perm.can_invite_users:
       await message.reply("You don't have enough rights to use this cmd:CanAddUsers")
       return
    link = await nora.export_chat_invite_link(message.chat.id)
    await message.reply(f"{link}", disable_web_page_preview=True)

@nora.on_message(cmd(["settitle", "title"]) & filters.group)
@adminsOnly
@selfadmin
async def settitle(perm, message):
    if not perm.can_promote_members:
       await message.reply("You don't have enough rights to use this cmd:CanAddAdmins")
       return
    if not message.reply_to_message:
       await message.reply("Reply to a user to set his custom admin title")
       return
    if len(message.command) == 1:
       await message.reply("Give a title to set it.")
       return

    user = message.reply_to_message.from_user.id
    title = message.command[1]

    try:
        await nora.set_administrator_title(message.chat.id, user, title)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    await message.reply("Succesfully changed {} admin title to {}".format(message.reply_to_message.from_user.mention, title))

ADMIN_TEXT = """
**✘ A module from which admins of the chat can use!**

‣ `?adminlist` - To get a list of admins of a chat.
‣ `?promote` - To Promote a user in the chat.
‣ `?demote` - To Demote a user in the chat.
‣ `?invitelink` - To get invitelink of a chat.
‣ `?admincache` - To refresh admin list.
‣ `?setgpic` - Changes the group of a chat.
‣ `?delgpic` - Deletes the current group pic.
‣ `?settitle` - sets the title of a admin.
"""
