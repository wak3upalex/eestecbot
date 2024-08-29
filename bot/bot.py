from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram import types
from aiogram.filters import Command
import os

import logging

logging.basicConfig(level=logging.INFO)
# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

from reg import *
from inLineButtons_quest import *
from buttons import *
@dp.message(Command(commands=["start"]))
async def start_command_handler(message: types.Message):
    logging.info('Start command received')
    await message.answer('Привет! Я бот-помощник сообщества EESTEC LC St. Petersburg!')

if __name__ == '__main__':
    dp.run_polling(bot)
