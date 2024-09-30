import asyncio

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
import httplib2
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from bot import bot, dp
import os
import json


class newsletter1States(StatesGroup):
    waiting_for_message1 = State()


@dp.message(Command(commands="SendToAll"))  # Обработка команды на запуск рассылки
async def process_SendToAll_command(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"]:  # Поиск админа по id
            if "role" in templates and templates["role"] == "Admin":  # Проверка роли
                await message.answer("Напишите текст для пользователей")
                await state.set_state(newsletter1States.waiting_for_message1)
            else:
                await message.answer("У Вас недостаточно прав")


@dp.message(newsletter1States.waiting_for_message1)  # Отправка сообщения пользователям
async def message_get1(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    user_count = 0
    sent_messages = {}  # Словарь для хранения ID сообщений

    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        sent_message = None

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
            user_count += 1

    # Сохранение информации о последних отправленных сообщениях
    await state.update_data(sent_messages=sent_messages)
    print(sent_messages)
    await message.answer(f"Сообщение было отправлено {user_count} пользователям.")
    await state.clear()


@dp.message(Command(commands="DeleteLastMessage"))
async def delete_last_message(message: Message, state: FSMContext):
    # Проверка прав доступа
    folder_path = 'users'
    for file_name in os.listdir(folder_path):
        with open(f"{folder_path}/{file_name}") as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"] and templates.get("role") == "Admin":
            # Права подтверждены, продолжаем удаление
            state_data = await state.get_data()
            sent_messages = state_data.get("sent_messages", {})

            for chat_id, message_id in sent_messages.items():
                try:
                    await message.bot.delete_message(chat_id=chat_id, message_id=message_id)
                    await message.answer("Последние сообщения удалены.")
                except Exception as e:
                    await message.answer(f"Не удалось удалить сообщение для пользователя {chat_id}: {e}")

            await message.answer("Последние сообщения удалены.")
            return

    # Если не админ
    await message.answer("У Вас недостаточно прав для выполнения этой команды.")


"""
class newsletterStates(StatesGroup):
    waiting_for_message = State()

@dp.message(Command(commands="SendToEESTECers")) # we implement the command to send messages only to EESTECers
async def process_SendEESTECers_command(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name) #

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"]:
            if "role" in templates:
                if templates["role"] == "LD" or templates["role"] == "VC" or templates["role"] == "Admin":
                    await message.answer("Напишите текст для пользователей")
                    await state.set_state(newsletterStates.waiting_for_message)
                else:
                    await message.answer("У Вас недостаточно прав")

@dp.message(newsletterStates.waiting_for_message)
async def message_get(message: Message, state:FSMContext):
    folder_path = 'users'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        if "role" in templates:
            if templates["role"] != "outmem":
                if message.text is not None:
                    await bot.send_message(chat, message.text)
                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                         caption=message.caption)
                elif message.document is not None:
                    await bot.send_document(chat_id=chat, document=message.document.file_id,
                                            caption=message.caption)


class newsletter1States(StatesGroup):
    waiting_for_message1 = State()

@dp.message(Command(commands="SendToAll"))
async def process_SendToAll_command(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"]:
            if "role" in templates:
                if templates["role"] == "PRL" or templates["role"] == "Admin":
                    await message.answer("Напишите текст для пользователей")
                    await state.set_state(newsletter1States.waiting_for_message1)
                else:
                    await message.answer("У Вас недостаточно прав")

@dp.message(newsletter1States.waiting_for_message1)
async def message_get1(message: Message, state:FSMContext):
    folder_path = 'users'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        if "role" in templates:
            if templates["role"] == "outmem":
                if message.text is not None:
                    await bot.send_message(chat, message.text)
                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                         caption=message.caption)
                elif message.document is not None:
                    await bot.send_document(chat_id=chat, document=message.document.file_id,
                                            caption=message.caption)
        else:
            if message.text is not None:
                await bot.send_message(chat, message.text)
            elif message.photo is not None:
                await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                     caption=message.caption)
            elif message.document is not None:
                await bot.send_document(chat_id=chat, document=message.document.file_id,
                                        caption=message.caption)

class newsletter2States(StatesGroup):
    waiting_for_message2 = State()
    waiting_for_message3 = State()
    waiting_for_message4 = State()
mrole = ""
@dp.message(Command(commands="SendToTeam"))
async def process_SendToTeam_command(message: Message, state: FSMContext):
    folder_path = 'users'
    file_names = []
    global mrole
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        if message.from_user.id == templates["id"]:
            if "role" in templates:
                if templates["role"] == "PRL" or templates["role"] == "ITL" or templates["role"] == "CRL" or templates["role"] == "HRL":
                    mrole=templates["role"]
                    await message.answer("Напишите текст для пользователей")
                    await state.set_state(newsletter2States.waiting_for_message2)
                elif templates["role"] == "Admin":
                    await message.answer("Какой команде хотите написать?\n Введите первы две заглавные буквы команды (пример: PR)")
                    await state.set_state(newsletter2States.waiting_for_message3)
                else:
                    await message.answer("У Вас недостаточно прав")

@dp.message(newsletter2States.waiting_for_message2)
async def message_get2(message: Message, state:FSMContext):
    folder_path = 'users'
    file_names = []
    global mrole
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        if "role" in templates:
            if templates["role"] == mrole[0] + mrole[1] or (templates["role"] == "Admin" and (mrole[0] + mrole[1]) == "IT"):
                if message.text is not None:
                    await bot.send_message(chat, message.text)
                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                         caption=message.caption)
                elif message.document is not None:
                    await bot.send_document(chat_id=chat, document=message.document.file_id,
                                            caption=message.caption)


@dp.message(newsletter2States.waiting_for_message3)
async def message_get3(message: Message, state:FSMContext):
    folder_path = 'users'
    file_names = []
    mrole = message.text
    await message.answer("Напишите текст для пользователей")
    await state.set_state(newsletter2States.waiting_for_message4)

@dp.message(newsletter2States.waiting_for_message4)
async def message_get4(message: Message, state:FSMContext):
    folder_path = 'users'
    file_names = []
    global mrole
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)

    for i in file_names:
        with open("users/" + i) as f:
            templates = json.load(f)
        chat = str(templates["id"])
        if "role" in templates:
            if templates["role"] == mrole[0] + mrole[1] or (templates["role"] == "Admin" and (mrole[0] + mrole[1]) == "IT"):
                if message.text is not None:
                    await bot.send_message(chat, message.text)
                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat, photo=message.photo[-1].file_id,
                                         caption=message.caption)
                elif message.document is not None:
                    await bot.send_document(chat_id=chat, document=message.document.file_id,
                                            caption=message.caption)
"""
