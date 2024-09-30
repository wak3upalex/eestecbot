import asyncio

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import Command
from bot import bot, dp
import os
import json


@dp.message(Command(commands="DeleteLastMessage"))
async def delete_last_message(message: Message):
    # Проверка прав доступа
    folder_path = 'users'
    for file_name in os.listdir(folder_path):
        with open(f"{folder_path}/{file_name}") as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"] and templates.get("role") == "Admin":
            # Права подтверждены, продолжаем удаление
            file_chatid = open("chatid.txt", "r")
            for i in file_chatid:
                chat_id = i[:i.find(" ")]
                message_id = i[i.find(" "):]
                try:
                    await message.bot.delete_message(chat_id=chat_id, message_id=message_id)
                    await message.answer("Последние сообщения удалены.")
                except Exception as e:
                    await message.answer(f"Не удалось удалить сообщение для пользователя {chat_id}: {e}")

            await message.answer("Последние сообщения удалены.")
            return

    # Если не админ
    await message.answer("У Вас недостаточно прав для выполнения этой команды.")