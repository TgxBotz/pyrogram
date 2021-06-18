from .. import *
import functools

async def is_admin_or_owner(message, user_id) -> bool:
    if message.chat.type in ["private", "bot"]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in ("creator", "administrator"):
        return True
    return False

def adminsOnly(func):
    @functools.wraps(func)
    async def magic_admin(client, message):
        if message.chat.type != "private":
          perms = await nora.get_chat_member(message.chat.id, message.from_user.id)
          is_a_o = await is_admin_or_owner(message, message.from_user.id)
          if is_a_o:
              await func(perms, message)
          else:
              await message.reply_text("Only admins can execute this command!")
        else:
            await message.reply("This cmd is made to be used in groups not in PM!")
    return magic_admin

def selfadmin(func):
    @functools.wraps(func)
    async def self(client, message):
      ad = await nora.get_chat_member(message.chat.id, 1813724543)
      if ad.status != "administrator":
          await message.reply("I need to be admin in the chat to perform this action\n__Mind promoting me?__")
      else:
          await func(client, message)
    return self

async def admind_res(message, user) -> bool:
    users = await message.chat.get_chat_member(int(user))
    if user.status in ("administrator", "creator"):
     return True
    return False
