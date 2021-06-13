from SpamBot.helpers.mongo import (
   add_warn,
   get_warn,
   int_to_alpha,
   remove_warns
)
from pyrogram.types import Message
from SpamBot.helpers.admins import adminsOnly, selfadmin
from .. import nora, cmd
from pyrogram import filters

async def list_admins(chat_id: int):
    list_of_admins = []
    async for member in nora.iter_chat_members(
        chat_id, filter="administrators"
    ):
        list_of_admins.append(member.user.id)
    return list_of_admins

async def list_members(group_id):
    list_of_members = []
    async for member in nora.iter_chat_members(group_id):
        list_of_members.append(member.user.id)
    return list_of_members

@nora.on_message(cmd("warn") & filters.group)
@selfadmin
@adminsOnly
async def warn(perm, message: Message):
    if not perm.can_restrict_members:
      await message.reply_text("You are missing the following rights to use this command:CanBanUsers")
      return
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to warn a user.")
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    
    if user_id == 1813724543:
        await message.reply_text("You want me to warn myself?")
    elif user_id in await list_admins(message.chat.id):
        await message.reply_text("Can't warn an admin.")
    else:
        if user_id in await list_members(chat_id):
            warns = await get_warn(chat_id, await int_to_alpha(user_id))
            if warns:
                warns = warns["warns"]
            else:
                warn = {"warns": 1}
                await add_warn(chat_id, await int_to_alpha(user_id), warn)
                return await message.reply_text(
                    f"Warned {mention} !, 1/3 warnings now."
                )
            if warns >= 2:
                await message.chat.kick_member(user_id)
                await message.reply_text(
                    f"Number of warns of {mention} exceeded, Banned!"
                )
                await remove_warns(chat_id, await int_to_alpha(user_id))
            else:
                warn = {"warns": warns + 1}
                await add_warn(chat_id, await int_to_alpha(user_id), warn)
                await message.reply_text(
                    f"Warned {mention} !, {warns+1}/3 warnings now."
                )
        else:
            await message.reply_text("This user isn't here.")

@nora.on_message(cmd("rmwarn") & filters.group)
@adminsOnly
@selfadmin
async def rmwarn(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this command:CanBanUsers")
      return
    if not message.reply_to_message:
      await message.reply("Reply to a user to remove his warn!")
      return

    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply(f"{mention} have no warnings.")
    else:
        warn = {"warns": warns - 1}
        await add_warn(chat_id, await int_to_alpha(user_id), warn)
        await message.reply(f"Removed last warning of {mention}.")

@nora.on_message(cmd("resetwarns") & filters.group)
@adminsOnly
@selfadmin
async def rmwarns(perm, message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this command:CanBanUsers")
      return
    if not message.reply_to_message:
      await message.reply("Reply to a user to remove his warn!")
      return
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply(f"{mention} have no warnings.")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply(f"Removed all warnings of {mention}.")

@nora.on_message(cmd("warns"))
@adminsOnly
@selfadmin
async def check_warns(perm, message: Message):
    if not perm.can_restrict_members:
      await message.reply("You are missing the following rights to use this command:CanBanUsers")
      return
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to check a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention_user = message.reply_to_message.from_user.mention
    mention_from_user = message.from_user.mention
    chat_id = message.chat.id
    if message.reply_to_message:
        warns = await get_warn(chat_id, await int_to_alpha(user_id))
        if warns:
            warns = warns["warns"]
        else:
            return await message.reply_text(
                f"{mention_user} have no warnings."
            )
        return await message.reply_text(
            f"{mention_user} have {warns}/3 warnings."
        )
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"{mention_user} have no warnings.")
    await message.reply_text(f"{mention_from_user} have {warns}/3 warnings.")
