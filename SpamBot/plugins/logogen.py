""" Logo Generator! """"

from pyrogram import filters
from .. import nora
from pyrogram.types import (
   InlineKeyboardButton, 
   InlineKeyboardMarkup,
   InlineQueryResultPhoto
)
from bs4 import *
import shutil
import requests
import os
import base64
import sys
import random
import requests

def download_images(images): 
    count = 0
    print(f"Total {len(images)} Image Found!") 
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = image["data-srcset"] 
            except: 
                try: 
                    image_link = image["data-src"] 
                except:
                    try:
                        image_link = image["data-fallback-src"] 
                    except:
                        try:
                            image_link = image["src"] 
                        except: 

                            pass
            try: 
                r = requests.get(image_link).content 
                try:

                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    with open("logo@FridayOT.jpg", "wb+") as f: 
                        f.write(r)
                    count += 1
            except: 
                pass


def mainne(name, typeo):
    url = f"https://www.brandcrowd.com/maker/logos?text={name}&searchtext={typeo}&searchService="
    r = requests.get(url) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    images = soup.findAll('img') 
    random.shuffle(images)
    if images is not None:
       print("level 1 pass")
    download_images(images)

@nora.on_inline_query(filters.regex("logogen"))
async def logogen(client, iq):
    try:
        input = iq.query.split(":", 1)
        name = input[0]
        typeo = input[1]
    except IndexError:
     await client.answer_inline_query(
       iq.id,
       cache_time=0,
       results=[],
       switch_pm_text="@ThePyroGramBot logogen [Text|Type]!",
       switch_pm_parameter="start"
     )
    mainne(name, typeo)
    results = []
    caption = "**Generated Logo By @ThePyroGramBot!**"
    pate = "logo@PyroGram.jpg"
    results.append(
     InlineQueryResultPhoto(
      title="Generated Logo!",
      description="Successfully Generated Logo!",
      photo_url=pate,
      caption=caption
    ))
    await client.answer_inline_query(iq.id, cache_time=0, results=results, switch_pm_text="Succesfully Generated Logo!", switch_pm_parameter="start")
