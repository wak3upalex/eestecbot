from aiogram import Bot
from aiogram.enums import ParseMode
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
keyboard = ReplyKeyboardMarkup(keyboard=[[button] for button in buttons],resize_keyboard=True)



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
    department = message.text


    if department == 'Board':
        await message.answer(
            text="*Board* состоит из руководителей нашего замечательного сообщества\! В него входят:\n"
                 "• Chairperson \(Руководитель Сообщества\)\n"
                 "• Vice\-Chairperson for Administrative Affairs \(Заместитель Руководителя по административным вопросам\)\n"
                 "• Contact Person \(Заместитель Руководителя по международным связям\)\n"
                 "• Treasurer \(Заместитель Руководителя по финансовым вопросам\)\n"
                 "• HR Team Leader\n"
                 "• PR Team Leader\n"
                 "• CR Team Leader\n"
                 "• IT Team Leader",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif department == 'IT':
        await message.answer(
            text="IT-отдел - это про сплоченное сообщество программистов, которые стремятся развивать свои soft и hard skills. Отдел предоставляет среду для командной разработки и развития навыков, необходимых для работы в IT-компании. Если ты любишь программирование, хочешь учиться и развиваться самостоятельно, а также вести активную студенческую жизнь, то смело выбирай IT!",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode = "Markdown"
        )
    elif department == 'PR':
        await message.answer(
            text="PR отдел формирует имидж сообщества в медиа, отвечает за насыщенный контент и визуальную составляющую. Ребята повышают узнаваемость и популярность сообщества, а также способствуют его развитию и росту. Если ты любишь социальные сети и творчество, умеешь работать в команде и всегда имеешь в запасе парочку клевых идей, то PR - для тебя!",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode = "Markdown"
        )
    elif department == 'CR':
        await message.answer(
            text="CR отдел - это работа с партнёрами: поиск предложений и возможных контактов, а так же проведение переговоров. Эти ребята поддерживают каждое событие в ячейке: от международных мероприятий до неформальных встреч. Если ты любишь психологию, хочешь научиться договариваться с людьми и готов идти напролом, то CR - идеальный вариант.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode = "Markdown"
        )
    elif department == 'HR':
        await message.answer(
            text="HR отдел - это работа с членами сообщества и участниками мероприятий. Помощь в адаптации новым мемберам, мотивация участников и организация мероприятий и выездов - всем этим занимаются в HR. Если ты активный, общительный и хочешь научиться организовывать мероприятия и создавать комфортную рабочую атмосферу, то тебе сюда!",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode = "Markdown"
        )
    else:
        await message.answer(
            text="Пожалуйста, выберите один из предложенных отделов используя кнопочки.",
            reply_markup=keyboard
        )
        return


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