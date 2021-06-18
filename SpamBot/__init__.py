import os
import logging
import time
from functools import partial
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Python_ARQ import ARQ
from aiohttp import ClientSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [Pyrogram] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.ERROR)


cmd = partial(filters.command, prefixes=list("!?/"))

API_KEY = 'ZGYYCU-UORQWA-OQCZFP-UXZLWI-ARQ'
aiohttpsession = ClientSession()
arq = ARQ("thearq.tech", API_KEY, aiohttpsession)

MONGO_URL = "mongodb+srv://pyrogram:pyrogram@cluster0.hph8v.mongodb.net/telegram?retryWrites=true&w=majority"
mongo = MongoClient(MONGO_URL)
db = mongo.pyro

APP_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
TOKEN = "1874283501:AAERQ-26DZ3eCdmVJyKFC70N7-NppcBk12k"
DB_URI = "postgres://tqorpxto:TfSx0WpsjqKSE2iGgrq-c0xk5Im-nryF@queenie.db.elephantsql.com:5432/tqorpxto"

START_TIME = time.time()
AUTH = [1569115700, 1207066133, 1167145475]

nora = Client(
   "nora",
   bot_token=TOKEN,
   api_id=APP_ID,
   api_hash=API_HASH,
)

