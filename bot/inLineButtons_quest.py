from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot import bot, dp


# Состояния
class TestStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

# Вопросы и ответы
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

@dp.message(Command("quest"))
async def start_test(message: types.Message, state: FSMContext):
    await message.answer("Правила: Вам будет задано 4 вопроса с вариантами ответов. Выберите один из вариантов.")
    user_answers[message.from_user.id] = []
    await ask_question(message, state, TestStates.Q1, 0)

async def ask_question(message: types.Message, state: FSMContext, state_name: State, question_index: int):
    question = questions[question_index]
    markup = ReplyKeyboardBuilder()

    for option in question["options"]:
        markup.add(KeyboardButton(text=option))

    await message.answer(question["question"], reply_markup=markup.as_markup(resize_keyboard=True, one_time_keyboard=True))
    await state.set_state(state_name)

@dp.message(StateFilter(TestStates.Q1))
async def process_q1(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await ask_question(message, state, TestStates.Q2, 1)

@dp.message(StateFilter(TestStates.Q2))
async def process_q2(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await ask_question(message, state, TestStates.Q3, 2)

@dp.message(StateFilter(TestStates.Q3))
async def process_q3(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await ask_question(message, state, TestStates.Q4, 3)

@dp.message(StateFilter(TestStates.Q4))
async def process_q4(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.clear()
    await calculate_result(message)

async def calculate_result(message: types.Message):
    answers = user_answers[message.from_user.id]
    # Подсчет количества ответов для каждой группы
    score = [0, 0, 0, 0]
    for i, answer in enumerate(answers):
        selected_index = questions[i]["options"].index(answer)
        score[selected_index] += 1

    # Определение группы с наибольшим количеством выборов
    result_index = score.index(max(score))
    result_group = results_map[result_index]

    await message.answer(f"Ваш результат: {result_group}")
