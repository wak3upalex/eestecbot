from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram import types
from aiogram.filters import Command
import os
import json
from datetime import datetime

import logging
log_file_path = 'logs_bot.log'  # Указываем имя файла для логов

# Создание обработчика для записи логов в файл на уровне WARNING и выше
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.WARNING)

# Создание обработчика для вывода логов в консоль на уровне INFO и выше
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Форматирование логов
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logging.basicConfig(level=logging.WARNING, handlers=[file_handler, console_handler])

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

    # Check if user file exists
    user_file_path = f'users/{message.from_user.username}.json'
    if os.path.exists(user_file_path):
        # Load existing user data
        with open(user_file_path, 'r') as infile:
            user_data = json.load(infile)
    else:
        # Create new user data
        user_data = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.language_code,
            "last_interaction_time": current_time,
            "quest_result": None  # Initialize quest_result field
        }

    # Update last interaction time
    user_data["last_interaction_time"] = current_time

    # Save updated user data back to JSON
    with open(user_file_path, 'w') as outfile:
        json.dump(user_data, outfile)

    logging.info('Start command received from user: %s', message.from_user.username)
    await message.answer('Привет! Я бот-помощник сообщества EESTEC LC St. Petersburg!')

if __name__ == '__main__':
    dp.run_polling(bot)
