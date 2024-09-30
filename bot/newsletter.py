import json
import os
import logging

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot import bot, dp

# Создание логгера для текущего модуля
logger = logging.getLogger(__name__)


class newsletter1States(StatesGroup):
    waiting_for_message1 = State()


@dp.message(Command(commands="SendToAll"))  # Обработка команды на запуск рассылки
async def process_SendToAll_command(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /SendToAll")

    try:
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(file_name)
    except FileNotFoundError:
        logger.error(f"Папка {folder_path} не найдена!")
        await message.answer(f"Ошибка: папка {folder_path} не найдена.")
        return

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"]:
            if "role" in templates and templates["role"] == "Admin":
                logger.info(f"Пользователь {message.from_user.username} имеет роль Admin")
                await message.answer("Напишите текст для пользователей")
                await state.set_state(newsletter1States.waiting_for_message1)
            else:
                logger.warning(
                    f"Пользователь {message.from_user.username} ({message.from_user.id}) пытался использовать рассылку, но не имеет прав")
                await message.answer("У Вас недостаточно прав")


@dp.message(newsletter1States.waiting_for_message1)  # Отправка сообщения пользователям
async def message_get1(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    user_count = 0
    sent_messages = {}

    logger.info(f"Начало рассылки сообщений от пользователя {message.from_user.username} ({message.from_user.id})")

    try:
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                file_names.append(file_name)
    except FileNotFoundError:
        logger.error(f"Папка {folder_path} не найдена!")
        await message.answer(f"Ошибка: папка {folder_path} не найдена.")
        return

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        sent_message = None

        try:
            # Отправка сообщения пользователям с ролями "outmem" и "Admin"
            if "role" in templates and (templates["role"] == "outmem" or templates["role"] == "Admin"):
                if message.text:
                    sent_message = await bot.send_message(chat, message.text)
                elif message.photo:
                    sent_message = await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                                        caption=message.caption)
                elif message.document:
                    sent_message = await bot.send_document(chat_id=chat, document=message.document.file_id,
                                                           caption=message.caption)

            # Отправка пользователям без роли
            elif "role" not in templates:
                if message.text:
                    sent_message = await bot.send_message(chat, message.text)
                elif message.photo:
                    sent_message = await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                                        caption=message.caption)
                elif message.document:
                    sent_message = await bot.send_document(chat_id=chat, document=message.document.file_id,
                                                           caption=message.caption)

            # Сохранение ID сообщения для удаления
            if sent_message:
                sent_messages[chat] = sent_message.message_id
                logger.info(f"Сообщение отправлено пользователю {chat}")
                user_count += 1
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения пользователю {chat}: {e}")

    # Сохранение информации о последних отправленных сообщениях
    await state.update_data(sent_messages=sent_messages)
    logger.info(f"Сообщения успешно отправлены {user_count} пользователям")
    await message.answer(f"Сообщение было отправлено {user_count} пользователям.")
    await state.clear()

