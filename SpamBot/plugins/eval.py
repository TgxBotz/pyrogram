import io
import subprocess
import sys
from pyrogram import filters

import traceback
import asyncio
from SpamBot import *
from SpamBot.helpers.admins import adminsOnly, selfadmin
from datetime import datetime
import re
from inspect import getfullargspec
from io import StringIO
from time import time

SUDO = [1704673514]

@nora.on_message(
   filters.user(SUDO)
   & cmd("e")
)
async def executor(client, message):
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexe(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**✘ PEval -**\n```{cmd}```\n\n**✘ OUTPUT**:\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        await message.reply_document(
            document=filename,
            caption=f"**INPUT:**\n`{cmd[0:980]}`\n\n**OUTPUT:**\n`Attached Document`",
            quote=False
        )
        await message.delete()
        os.remove(filename)
    else:
        await message.reply(final_output)


async def aexe(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@nora.on_message(
   cmd("bash")
   & filters.user(SUDO)
)
async def sed_terminal(client, message):
    stark = await message.reply("`Processing........`")
    if len(message.command) == 1:
        await stark.edit(
            "`Please Give Me A Bash Code To Execute`"
        )
        return
    cmd = message.text.split(None, 1)[1]
    if message.reply_to_message:
        message.reply_to_message.message_id

    pid, err, out, ret = await run_command(cmd)
    if not out:
        out = "No OutPut!"
    friday = f"""
**➥Bash :**
`{cmd}`

**➥Output :**
`{out}`
"""
    await stark.edit(friday)


async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    errors = stderr.decode()
    if not errors:
        errors = "No Errors!"
    output = stdout.decode()
    return process.pid, errors, output, process.returncode


@nora.on_message(cmd("delgpic"))
@adminsOnly
@selfadmin
async def delgpic(perm, message):
    if not perm.can_change_info:
      await message.reply(
        "You are missing the following rights to use this cmd:CanChangeInfo")
      return
    try:
       await nora.delete_chat_photo(message.chat.id)
    except BaseException as be:
        await message.reply(f"**Error:**\n`{be}`")
        return
    await message.reply('Succesfully removed group pic')
