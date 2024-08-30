from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot import bot, dp


# Состояния
class TestStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()


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
    },
    {
        "question" : "Вопрос 5",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },
    {
        "question" : "Вопрос 6",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },
    {
        "question" : "Вопрос 7",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },
    {
        "question" : "Вопрос 8",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },
    {
        "question" : "Вопрос 9",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },
    {
        "question" : "Вопрос 10",
        "options" : ["Ответ 1","Ответ 2","Ответ 3","Ответ 4"]
    },

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
    await message.answer("Правила: Вам будет задано 10 вопросов с вариантами ответов. Выберите один из вариантов.")
    user_answers[message.from_user.id] = []
    await ask_question(message, state, TestStates.Q1, 0)

async def ask_question(message: types.Message, state: FSMContext, state_name: State, question_index: int):
    question = questions[question_index]
    markup = ReplyKeyboardBuilder()

    for option in question["options"]:
        markup.row(KeyboardButton(text=option))

    await message.answer(question["question"], reply_markup=markup.as_markup(resize_keyboard=True, one_time_keyboard=False))
    await state.set_state(state_name)

async def handle_answer(message: types.Message, state: FSMContext, next_state: State, question_index: int):
    user_input = message.text
    correct_options = questions[question_index]["options"]
    if user_input not in correct_options:
        print(f"Некорректный ответ от пользователя {message.from_user.id}: {user_input}.")
        await message.answer("Пожалуйста, выберите один из предложенных вариантов ответа.")
        return
    user_answers[message.from_user.id].append(user_input)
    await ask_question(message, state, next_state, question_index + 1)
@dp.message(StateFilter(TestStates.Q1))
async def process_q1(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q2, 0)

@dp.message(StateFilter(TestStates.Q2))
async def process_q2(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q3, 1)

@dp.message(StateFilter(TestStates.Q3))
async def process_q3(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q4, 2)

@dp.message(StateFilter(TestStates.Q4))
async def process_q4(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q5, 3)

@dp.message(StateFilter(TestStates.Q5))
async def process_q5(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q6, 4)

@dp.message(StateFilter(TestStates.Q6))
async def process_q6(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q7, 5)

@dp.message(StateFilter(TestStates.Q7))
async def process_q7(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q8, 6)

@dp.message(StateFilter(TestStates.Q8))
async def process_q8(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q9, 7)

@dp.message(StateFilter(TestStates.Q9))
async def process_q9(message: types.Message, state: FSMContext):
    await handle_answer(message, state, TestStates.Q10, 8)

@dp.message(StateFilter(TestStates.Q10))
async def process_q10(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await state.clear()
    await calculate_result(message)



async def calculate_result(message: types.Message):
    answers = user_answers[message.from_user.id]
    score = [0, 0, 0, 0]

    for i, answer in enumerate(answers):
        selected_index = questions[i]["options"].index(answer)
        score[selected_index] += 1

    max_score = max(score)
    result_groups = [results_map[i] for i, s in enumerate(score) if s == max_score]

    result_text = "Ваш результат: " + " и ".join(result_groups)
    await message.answer(result_text, reply_markup=ReplyKeyboardRemove())

