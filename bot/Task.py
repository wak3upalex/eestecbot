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

BOT_TOKEN = ''
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
waiting_for_tea=""

def get_pos_for_open(pos, what):
    if what=="none":
        if "ITL" in pos:
            return "IT"
        elif "HRL" in pos:
            return "HR"
        elif "PRL" in pos:
            return "PR"
        elif "CRL" in pos:
            return "CR"
        elif "LD" in pos:
            return "LD"
        else:
            return "0"
    elif what=="1":
        if "ITL" in pos:
            return "IT"
        elif "HRL" in pos:
            return "HR"
        elif "PRL" in pos:
            return "PR"
        elif "CRL" in pos:
            return "CR"
        elif "LD" in pos:
            return "LD"
        elif "IT" in pos:
            return "it"
        elif "PR" in pos:
            return "pr"
        elif "CR" in pos:
            return "cr"
        elif "HR" in pos:
            return "hr"
        else:
            return "0"
    else:
        if "ITL" in pos:
            if (what == "1"):
                return "ITtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "HRL" in pos:
            if (what == "1"):
                return "HRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "PRL" in pos:
            if (what == "1"):
                return "PRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "CRL" in pos:
            if (what == "1"):
                return "CRtasks.txt"
            else:
                return "Boardtasks.txt"
        elif "LD" in pos:
            if (what == "1"):
                return "ITtasks.txt"
            elif (what == "2"):
                return "HRtasks.txt"
            elif what == "3":
                return "PRtasks.txt"
            elif what == "4":
                return "CRtasks.txt"
            else:
                return "Boardtasks.txt"
def process_text(message):
    model = message.text
    file = open("users.txt", "a")
    file.write(model)
    file.write("\n")
    file.close()

"""this script remove task from list of tasks"""
class RemoveStates(StatesGroup):
    waiting_for_team = State()
    waiting_for_taskname = State()
@dp.message(Command(commands=['removeTasks']))
async def process_remove_command(message: Message, state:FSMContext):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = "none"
    bol = get_pos_for_open(bol, what)
    if bol != "0":
        if bol == "IT":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "HR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "PR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "CR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "LD":
            await message.answer(
                "Напишите 1 Если для IT команды\n"
                "Напишите 2 Если для HR команды\n"
                "Напишите 3 Если для PR команды\n"
                "Напишите 4 Если для CR команды\n"
                "Напишите 5 Если это для борда"
            )
        await state.set_state(RemoveStates.waiting_for_team)
    else:
        await bot.send_message(message.chat.id, "У вас нету прав для добавления тасков")
@dp.message(RemoveStates.waiting_for_team)
async def team_getr(message: Message, state:FSMContext):
    global waiting_for_tea
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = message.text
    bol = get_pos_for_open(bol, what)
    waiting_for_tea = bol
    await state.update_data(waiting_for_team = bol)
    await bot.send_message(message.chat.id, "Напишите название таска которого нужно удалить(Нужно писать точь-в-точь")
    await state.set_state(RemoveStates.waiting_for_taskname)
@dp.message(RemoveStates.waiting_for_taskname)
async def task_getr(message: Message, state:FSMContext):
    task = message.text
    with open(waiting_for_tea) as f:
        lines = f.readlines()
    pattern = re.compile(re.escape(task))
    with open(waiting_for_tea, 'w') as f:
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)
    await bot.send_message(message.chat.id, "Задача успешно удалена")
    await state.update_data(waiting_for_task=task)
    await state.clear()

"""this script add task to task file"""
class addTaskStates(StatesGroup):
    waiting_for_team = State()
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_person = State()
@dp.message(Command(commands=['addTasks']))
async def process_addTasks_command(message:Message, state: FSMContext):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = "none"
    bol = get_pos_for_open(bol,what)
    if bol != "0":
        if bol == "IT":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "HR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "PR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "CR":
            await bot.send_message(message.chat.id, "Напишите 1. Если для команды и 2. Если это для борда")
        elif bol == "LD":
            await message.answer(
                "Напишите 1 Если для IT команды\n"
                "Напишите 2 Если для HR команды\n"
                "Напишите 3 Если для PR команды\n"
                "Напишите 4 Если для CR команды\n"
                "Напишите 5 Если это для борда"
            )
        await state.set_state(addTaskStates.waiting_for_team)
    else:
        await bot.send_message(message.chat.id, "У вас нету прав для добавления тасков")

@dp.message(addTaskStates.waiting_for_team)
async def team_get(message: Message, state:FSMContext):
    global waiting_for_tea
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    what = message.text
    bol = get_pos_for_open(bol, what)
    waiting_for_tea = bol
    await state.update_data(waiting_for_team = bol)
    await bot.send_message(message.chat.id, "Напишите сам таск")
    await state.set_state(addTaskStates.waiting_for_task)
@dp.message(addTaskStates.waiting_for_task)
async def task_get(message: Message, state:FSMContext):
    task = message.text
    file = open(waiting_for_tea, "a")
    file.write(task)
    file.write('.')
    file.close()
    await bot.send_message(message.chat.id, "Напишите дедлайн таска в формате: дата-месяц-год время")
    await state.update_data(waiting_for_task=task)
    await state.set_state(addTaskStates.waiting_for_date)

@dp.message(addTaskStates.waiting_for_date)
async def date_get(message: Message, state: FSMContext):
    date = message.text
    file = open(waiting_for_tea, "a")
    file.write(date)
    file.write('.')
    file.close()
    await bot.send_message(message.chat.id, "Напишите кто ответсвеннен за задание в виде ФИ")
    await state.update_data(waiting_for_date=date)
    await state.set_state(addTaskStates.waiting_for_person)

@dp.message(addTaskStates.waiting_for_person)
async def person_get(message: Message, state:FSMContext):
    person = message.text
    file = open(waiting_for_tea, "a")
    file.write(person)
    file.write('\n')
    file.close()
    idfrom = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if person in line:
            bol = line
            break
    file.close()
    await bot.send_message(message.chat.id, "Таск добавлен")
    await state.update_data(waiting_for_person=person)
    await state.clear()
    await asyncio.create_task(notice(bol,waiting_for_tea,idfrom))


"""this script notifies about task"""
async def notice(id,fil,idfrom):
    file = open(fil, "r")
    dat = "none"
    task = ""
    name = id[id.find(" ")+1:id.rfind(" ")]
    for line in file:
        if name in line:
            dat = line[line.find(".")+1:line.rfind(".")]
            task = line[:line.find(".")]
    counter = 0
    send = 0
    results = [dat[:dat.find("-")], dat[dat.find("-")+1:dat.rfind("-")], dat[dat.rfind("-")+1:dat.rfind(" ")], dat[dat.rfind(" "):dat.rfind(":")], dat[dat.rfind(":")+1:]]
    deadlinetime = list(map(int, results))
    while (counter != 3):
        current_datetime = datetime.now()
        if counter == 1 and send == 0:
            await bot.send_message(id[:id.find(" ")], "Дедлайны горят, дедлайн наступит через 3 дня. По таску: " + task)
            await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончится через 3 дня, ответсвенный за неё " + name)
            send = 1
        elif counter == 2 and send == 1:
            await bot.send_message(id[:id.find(" ")], "Дедлайн уже завтра!!! По таску: " + task)
            await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончится через завтра, ответсвенный за неё " + name)
        if (int(current_datetime.year) - deadlinetime[2] == 0):
            if (int(current_datetime.month) - deadlinetime[1] == 0):
                if (int(current_datetime.day) - deadlinetime[0] == 3):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 1
                elif (int(current_datetime.day) - deadlinetime[0] == 1):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 2
                            send = 1
                elif (int(current_datetime.day) - deadlinetime[0] == 0):
                    if (int(current_datetime.hour) - deadlinetime[3] == 0):
                        if (int(current_datetime.minute) - deadlinetime[4] == 0):
                            counter = 3

    await bot.send_message(id[:id.find(" ")], "Время на выполнение задачи " + task + " истекло")
    await bot.send_message(idfrom, "Дедлайн по задаче " + task + " закончился, ответсвенный за неё " + name + ". Если она выполнена, то удалите пожалуйста данную задачу из списка тасков и поставте такому хорошему человеку + KPI=)")



"""this script show all task"""
@dp.message(Command(commands=['Tasks']))
async def process_Tasks_command(message:Message):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    if "IT" in bol:
        file = open("ITtasks.txt", "r")
        await bot.send_message(message.chat.id, "IT Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        if "ITL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "HR" in bol:
        file = open("HRtasks.txt", "r")
        await bot.send_message(message.chat.id, "HR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        if "HRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "PR" in bol:
        await bot.send_message(message.chat.id, "PR Команды таски:")
        file = open("PRtasks.txt", "r")
        for line in file:
            await message.answer(line)
        file.close()
        if "PRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "CR" in bol:
        await bot.send_message(message.chat.id, "CR Команды таски:")
        file = open("CRtasks.txt", "r")
        for line in file:
            await message.answer(line)
        file.close()
        if "CRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id,"Board таски:")
            for line in file:
                await message.answer(line)
            file.close()
    elif "LD" in bol:
        file = open("ITtasks.txt", "r")
        await bot.send_message(message.chat.id, "IT Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("HRtasks.txt", "r")
        await bot.send_message(message.chat.id, "HR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("CRtasks.txt", "r")
        await bot.send_message(message.chat.id, "CR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("PRtasks.txt", "r")
        await bot.send_message(message.chat.id, "PR Команды таски:")
        for line in file:
            await message.answer(line)
        file.close()
        file = open("Boardtasks.txt", "r")
        await bot.send_message(message.chat.id,"Board таски:")
        for line in file:
            await message.answer(line)
        file.close()
    else:
        await bot.send_message(message.chat.id, "Вы долны зарегистрироваться для просмотра тасков через /reg")


"""this script show your tasks"""
@dp.message(Command(commands=['mytasks']))
async def process_mytasks_command(message: Message):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    name = "none"
    for line in file:
        if id in line:
            bol = line
            name = line[line.find(" ")+1:line.rfind(" ")]
            break
    file.close()
    if "IT" in bol:
        file = open("ITtasks.txt", "r")
        await bot.send_message(message.chat.id, "IT Команды таски, за которые вы ответсвенны:")
        for line in file:
            if name in line:
                await message.answer(line)
        file.close()
        if "ITL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id, "Board таски, за которые вы ответсвенны:")
            for line in file:
                if name in line:
                    await message.answer(line)
            file.close()
    elif "HR" in bol:
        file = open("HRtasks.txt", "r")
        await bot.send_message(message.chat.id, "HR Команды таски, за которые вы ответсвенны:")
        for line in file:
            if name in line:
                await message.answer(line)
        file.close()
        if "HRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id, "Board таски, за которые вы ответсвенны:")
            for line in file:
                if name in line:
                    await message.answer(line)
            file.close()
    elif "PR" in bol:
        await bot.send_message(message.chat.id, "PR Команды таски, за которые вы ответсвенны:")
        file = open("PRtasks.txt", "r")
        for line in file:
            if name in line:
                await message.answer(line)
        file.close()
        if "PRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id, "Board таски, за которые вы ответсвенны:")
            for line in file:
                if name in line:
                    await message.answer(line)
            file.close()
    elif "CR" in bol:
        await bot.send_message(message.chat.id, "CR Команды таски, за которые вы ответсвенны:")
        file = open("CRtasks.txt", "r")
        for line in file:
            if name in line:
                await message.answer(line)
        file.close()
        if "CRL" in bol:
            file = open("Boardtasks.txt", "r")
            await bot.send_message(message.chat.id, "Board таски, за которые вы ответсвенны:")
            for line in file:
                if name in line:
                    await message.answer(line)
            file.close()
    elif "LD" in bol:
        file = open("Boardtasks.txt", "r")
        await bot.send_message(message.chat.id, "Board таски, за которые вы ответсвенны:")
        for line in file:
            if name in line:
                await message.answer(line)
        file.close()
    else:
        await bot.send_message(message.chat.id, "Вы долны зарегистрироваться для просмотра своих тасков через /reg")

"""this script send album"""
@dp.message(Command(commands=['Photo']))
async def process_Photo_command(message:Message):
    await message.answer('https://vk.com/albums-174856092')


dp.message.register(process_Tasks_command, Command(commands='Tasks'))
dp.message.register(process_addTasks_command, Command(commands='addTasks'))
dp.message.register(process_remove_command,Command(commands='removeTasks'))
dp.message.register(process_Photo_command, Command(commands='Photo'))

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
