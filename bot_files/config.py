import os

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from dotenv import load_dotenv

load_dotenv()

__BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=__BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
ADMINISTRATORS = 5610895802,
