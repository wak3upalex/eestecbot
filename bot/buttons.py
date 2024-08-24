from aiogram import Bot,  F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.types import BotCommand
from bot import bot, dp

class AboutUsStates(StatesGroup) :
    WaitingForDepartmentChoice = State()


departments = ["Board", "IT", "PR", "CR", "HR"]
buttons = [KeyboardButton(text=text) for text in departments]
keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

# Обработчик команды /help
@dp.message(Command(commands='help'))
async def help_command(message:Message):
    await message.answer(
        text='/about_us - Команда, которая расскажет тебе про наши отделы'
        '\n/quest - Пройди квест для определения своего отдела'
            # '\n/reg - Команда, которая поможет тебе зарегистрироваться в нашем в боте'
    )

# Обработчик команды /about_us
@dp.message(Command(commands='about_us'))
async def about_us(message:Message, state: FSMContext):
    await message.answer(
        text='Про какой отдел хочешь узнать?',
        reply_markup=keyboard
    )
    await state.set_state(AboutUsStates.WaitingForDepartmentChoice)

# Обработчик для всех департаментов
@dp.message(StateFilter(AboutUsStates.WaitingForDepartmentChoice))
async def process_department_choice(message: Message, state: FSMContext):
    department = message.text  # Получаем текст сообщения пользователя

    # Проверяем текст и отвечаем соответственно
    if department == 'Board':
        await message.answer(
            text="Board = Крутой отдел",
            reply_markup=ReplyKeyboardRemove()
        )
    elif department == 'IT':
        await message.answer(
            text="IT = Крутой отдел.",
            reply_markup=ReplyKeyboardRemove()
        )
    elif department == 'PR':
        await message.answer(
            text="PR = Крутой отдел.",
            reply_markup=ReplyKeyboardRemove()
        )
    elif department == 'CR':
        await message.answer(
            text="CR = Крутой отдел.",
            reply_markup=ReplyKeyboardRemove()
        )
    elif department == 'HR':
        await message.answer(
            text="HR = Крутой отдел.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="Пожалуйста, выберите один из предложенных отделов используя кнопочки.",
            reply_markup=keyboard
        )
        return  # Возвращаемся, чтобы не сбрасывать состояние

    # Сбрасываем состояние после успешного ответа
    await state.clear()

#menu
async def set_main_menu(bot:Bot):
    main_menu_commands = [
        BotCommand(command='/start',description='Ah Shit,here we go again.'),
        BotCommand(command='/help',description= 'Справка по работе бота'),
        BotCommand(command='/about_us',description='Команда, которая расскажет тебе про наши отделы'),
        BotCommand(command='/quest',description= 'Пройди квест для определения своего отдела'),
    ]
    await bot.set_my_commands(main_menu_commands)
dp.startup.register(set_main_menu)