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
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import creds
import logging
import re
from datetime import datetime

import os
from bot import bot, dp


def ensure_file_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass  # The file is now created.
class RegistrationStates(StatesGroup):
    waiting_for_namesirname = State()
    waiting_for_pos = State()
@dp.message(Command(commands=['reg']))
async def process_reg_command(message: Message, state: FSMContext):
    ensure_file_exists('users.txt')
    id = message.chat.id
    file = open("users.txt", "r")
    notreg = 1
    for line in file:
        if str(id) in line:
            notreg = 0
            await bot.send_message(message.chat.id, "Вы уже зарегистрированны")
    file.close()
    if notreg == 1:
        file = open("users.txt", "a")
        file.write(str(id))
        file.write(' ')
        file.close()
        await bot.send_message(message.chat.id, "Укажите вашу Фамилию и Имя")
        await state.set_state(RegistrationStates.waiting_for_namesirname)  # Устанавливаем состояние

@dp.message(RegistrationStates.waiting_for_namesirname)
async def name_get(message: Message, state:FSMContext):
    name = message.text
    file = open("users.txt", "a")
    file.write(name)
    file.write(' ')
    file.close()
    await bot.send_message(message.chat.id, "Укажите секретный код, если его нету напишите 0")
    await state.update_data(waiting_for_namesirname=name)
    await state.set_state(RegistrationStates.waiting_for_pos)

@dp.message(RegistrationStates.waiting_for_pos)
async def pos_get(message: Message, state:FSMContext):
    pos = message.text
    if (pos == 'ITld20786'):
        file = open("users.txt", "a")
        file.write('ITL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый IT лидер")
    elif (pos == 'CRld20800'):
        file = open("users.txt", "a")
        file.write('CRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый CR лидер")
    elif (pos == 'HRld29039'):
        file = open("users.txt", "a")
        file.write('HRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый HR лидер")
    elif (pos == 'PRld28473'):
        file = open("users.txt", "a")
        file.write('PRL')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый PR лидер")
    elif (pos == 'ChairP93827'):
        file = open("users.txt", "a")
        file.write('LD')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый стул")
    elif (pos == 'VC93827'):
        file = open("users.txt", "a")
        file.write('VC')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно, желаю исполнить все поставленные задачи новый стул")
    elif (pos == 'IT'):
        file = open("users.txt", "a")
        file.write('IT')
        file.write('\n')
        file.close()
    elif (pos == 'CR'):
        file = open("users.txt", "a")
        file.write('CR')
        file.write('\n')
        file.close()
    elif (pos == 'HR'):
        file = open("users.txt", "a")
        file.write('HR')
        file.write('\n')
        file.close()
    elif (pos == 'PR'):
        file = open("users.txt", "a")
        file.write('PR')
        file.write('\n')
        file.close()
    else:
        file = open("users.txt", "a")
        file.write('outmem')
        file.write('\n')
        file.close()
        await message.reply("Регистрация прошла успешно")
    await state.clear()


dp.message.register(process_reg_command, Command(commands='reg'))
