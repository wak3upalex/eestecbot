# I want to create a Python telegram bot,which will use aiogram library and  will say hello on each message

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

if __name__ == '__main__':
    dp.run_polling(bot)
