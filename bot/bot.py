from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

import logging

logging.basicConfig(level=logging.INFO)
# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

if __name__ == '__main__':
    dp.run_polling(bot)
