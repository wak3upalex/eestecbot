from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand
from bot import bot, dp


departments = ["Board", "IT", "PR", "CR", "HR"]
buttons = [KeyboardButton(text=text) for text in departments]
keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

# Обработчик команды /help
@dp.message(Command(commands='help'))
async def help_command(message:Message):
    await message.answer(
        text='/about_us - Команда, которая расскажет тебе про наши отделы'
             '\n/reg - Команда, которая поможет тебе зарегистрироваться в нашем в боте'
    )

# Обработчик команды /about_us
@dp.message(Command(commands='about_us'))
async def about_us(message:Message):
    await message.answer(
        text='Про какой отдел хочешь узнать?',
        reply_markup=keyboard
    )


# Ответ на Board
@dp.message(F.text == 'Board')
async def process_Board_answer(message: Message):
    await message.answer(
        text="Board = круто",
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на IT
@dp.message(F.text == 'IT')
async def process_IT_answer(message: Message):
    await message.answer(
        text="IT = круто",
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на PR
@dp.message(F.text == 'PR')
async def process_PR_answer(message: Message):
    await message.answer(
        text="PR = круто",
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на CR
@dp.message(F.text == 'CR')
async def process_CR_answer(message: Message):
    await message.answer(
        text="CR = круто",
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на HR
@dp.message(F.text == 'HR')
async def process_HR_answer(message: Message):
    await message.answer(
        text="HR = круто",
        reply_markup=ReplyKeyboardRemove()
    )
#menu
async def set_main_menu(bot:Bot):
    main_menu_commands = [
        BotCommand(command='/start',description='Ah Shit,here we go again.'),
        BotCommand(command='/help',description= 'Справка по работе бота'),
        BotCommand(command='/about_us',description='Команда, которая расскажет тебе про наши отделы')
    ]
    await bot.set_my_commands(main_menu_commands)
dp.startup.register(set_main_menu)