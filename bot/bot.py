from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram import types
from aiogram.filters import Command
import os
import json
from datetime import datetime

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
    # Ensure the 'users' directory exists
    if not os.path.exists('users'):
        os.makedirs('users')

    current_time = datetime.now().isoformat()
    # Save user data in JSON format in the 'users' directory
    user_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "language_code": message.from_user.language_code,
        "message_id": message.message_id,
        "last_interaction_time": current_time
    }
    with open(f'users/{message.from_user.username}.json', 'w') as outfile:
        json.dump(user_data, outfile)

    logging.info('Start command received')
    await message.answer('Привет! Я бот-помощник сообщества EESTEC LC St. Petersburg!')

if __name__ == '__main__':
    dp.run_polling(bot)
