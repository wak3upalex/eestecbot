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

BOT_TOKEN = '6430127705:AAEPvaAi2Z2Z7Epwop7DiGVvEpmuOQ8oGu8'
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
r = 0
itpoint=0
hrpoint=0
crpoint=0
prpoint=0
class QuestStates(StatesGroup):
    waiting_for_fq = State()
    waiting_for_sq = State()
    waiting_for_tq = State()
    waiting_for_foq = State()
    waiting_for_fisq = State()
    waiting_for_sixq = State()
    waiting_for_sevq = State()
    waiting_for_esq = State()
    waiting_for_nsq = State()
    waiting_for_tsq = State()

@dp.message(Command(commands=['quest']))
async def process_quest_command(message: Message, state: FSMContext):
    await message.answer(
        "Правила..."
    )
    await message.answer("1. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
    await state.set_state(QuestStates.waiting_for_fq)

@dp.message(QuestStates.waiting_for_fq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    r=0
    itpoint = 0
    hrpoint = 0
    crpoint = 0
    prpoint = 0
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r=1
    if r!=1:
        await message.answer("2. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_sq)
async def sq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_sq=answer)
        await state.set_state(QuestStates.waiting_for_tq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_sq=answer)
        await state.set_state(QuestStates.waiting_for_tq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_sq=answer)
        await state.set_state(QuestStates.waiting_for_tq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_sq=answer)
        await state.set_state(QuestStates.waiting_for_tq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("3. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_tq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_tq=answer)
        await state.set_state(QuestStates.waiting_for_foq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_tq=answer)
        await state.set_state(QuestStates.waiting_for_foq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_tq=answer)
        await state.set_state(QuestStates.waiting_for_foq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_tq=answer)
        await state.set_state(QuestStates.waiting_for_foq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("4. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_foq)
async def foq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_foq=answer)
        await state.set_state(QuestStates.waiting_for_fisq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_foq=answer)
        await state.set_state(QuestStates.waiting_for_fisq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_foq=answer)
        await state.set_state(QuestStates.waiting_for_fisq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_foq=answer)
        await state.set_state(QuestStates.waiting_for_fisq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("5. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_fisq)
async def fisq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_fisq=answer)
        await state.set_state(QuestStates.waiting_for_sixq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_fisq=answer)
        await state.set_state(QuestStates.waiting_for_sixq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_fisq=answer)
        await state.set_state(QuestStates.waiting_for_sixq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_fisq=answer)
        await state.set_state(QuestStates.waiting_for_sixq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("6. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_sixq)
async def ssq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_sixq=answer)
        await state.set_state(QuestStates.waiting_for_sevq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_sixq=answer)
        await state.set_state(QuestStates.waiting_for_sevq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_sixq=answer)
        await state.set_state(QuestStates.waiting_for_sevq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_sixq=answer)
        await state.set_state(QuestStates.waiting_for_sevq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("7. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_sevq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_sevq=answer)
        await state.set_state(QuestStates.waiting_for_esq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_sevq=answer)
        await state.set_state(QuestStates.waiting_for_esq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_sevq=answer)
        await state.set_state(QuestStates.waiting_for_esq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_sevq=answer)
        await state.set_state(QuestStates.waiting_for_esq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("8. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_esq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_esq=answer)
        await state.set_state(QuestStates.waiting_for_nsq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_esq=answer)
        await state.set_state(QuestStates.waiting_for_nsq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_esq=answer)
        await state.set_state(QuestStates.waiting_for_nsq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_esq=answer)
        await state.set_state(QuestStates.waiting_for_nsq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r = 1
    if r!=1:
        await message.answer("9. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_nsq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_nsq=answer)
        await state.set_state(QuestStates.waiting_for_tsq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_nsq=answer)
        await state.set_state(QuestStates.waiting_for_tsq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_nsq=answer)
        await state.set_state(QuestStates.waiting_for_tsq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_nsq=answer)
        await state.set_state(QuestStates.waiting_for_tsq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r=1

    if (r != 1):
        await message.answer("10. Вопрос...\n"
                         "1. Ответ\n"
                         "2. Ответ\n"
                         "3. Ответ\n"
                         "4. Ответ\n")
@dp.message(QuestStates.waiting_for_tsq)
async def fq_get(message: Message, state:FSMContext):
    answer = message.text
    global itpoint
    global prpoint
    global crpoint
    global hrpoint
    global r
    if(answer=="1"):
        itpoint = itpoint+1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer=="2"):
        hrpoint = hrpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer == "3"):
        crpoint = crpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    elif (answer == "4"):
        prpoint = prpoint + 1
        await state.update_data(waiting_for_fq=answer)
        await state.set_state(QuestStates.waiting_for_sq)
    else:
        await message.answer("Вы не правильно ввели ответ на вопрос")
        await state.clear()
        r=1
    await state.clear()
    if (itpoint>=hrpoint and itpoint>=crpoint and itpoint>=prpoint and r!=1):
        await message.answer("Идите в it")
    elif (hrpoint>=itpoint and hrpoint>=crpoint and hrpoint>=prpoint and r!=1):
        await message.answer("Идите в hr")
    elif (crpoint>=itpoint and crpoint>=hrpoint and crpoint>=prpoint and r!=1):
        await message.answer("Идите в hr")
    elif (prpoint>=itpoint and prpoint>=crpoint and prpoint>=hrpoint and r!=1):
        await message.answer("Идите в hr")
dp.message.register(process_quest_command, Command(commands='quest'))
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(dp.start_polling(bot))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
