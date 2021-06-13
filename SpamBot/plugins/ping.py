import time 
from SpamBot.helpers.ping_time import get_readable_time
from SpamBot import START_TIME
from datetime import datetime
from .. import nora, cmd

@nora.on_message(cmd("ping"))
async def ping(client, message):
    start = datetime.now()
    uptime = get_readable_time((time.time() - START_TIME))
    end = datetime.now()
    du = (end - start).microseconds / 1000
    await message.reply(f"**Pong:** __{du}__\n**Uptime:** __{uptime}__")
