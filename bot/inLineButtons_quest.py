from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot import bot, dp
# Состояния
class TestStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

# Данные для теста
questions = [
    {
        "question": "Что вам больше нравится?",
        "options": ["Работать с кодом", "Писать пресс-релизы", "Работать с клиентами", "Заниматься подбором персонала"]
    },
    {
        "question": "Какой тип работы вам ближе?",
        "options": ["Создание приложений", "Организация мероприятий", "Общение с клиентами", "Управление кадрами"]
    },
    {
        "question": "Какую задачу вы бы предпочли?",
        "options": ["Решить проблему с кодом", "Написать статью", "Провести переговоры", "Провести собеседование"]
    },
    {
        "question": "Какую область вы хотите развивать?",
        "options": ["IT", "PR", "CR", "HR"]
    }
]

results_map = {
    0: "IT",
    1: "PR",
    2: "CR",
    3: "HR"
}

user_answers = {}

@dp.message(Command(commands=['bquest']))
async def start_test(message: types.Message):
    await message.answer("Правила: Вам будет задано 4 вопроса с вариантами ответов. Выберите один из вариантов.")
    user_answers[message.from_user.id] = []
