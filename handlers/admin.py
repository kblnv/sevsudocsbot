# Файл, содержащий админские обработчики

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
 
from keyboards import user
from database import db

class CategoryAddFSM(StatesGroup):
    category_title = State()

class CategoryDeleteFSM(StatesGroup):
    category_title = State()

class QuestionAddFSM(StatesGroup):
    category_title = State()
    question_title = State()
    question_description = State()

class QuestionDeleteFSM(StatesGroup):
    question_title = State()

async def add_category_command_handler(message: types.Message):
    """ Обработчик комманды /add_category
        Начало ввода данных для добавления категории
    """
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Отмена"))

    # Устанавливаем ожидание ввода названия категории
    await CategoryAddFSM.category_title.set()
    await message.answer("Введите название категории:", reply_markup=markup)

async def add_category_title_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее название категории """
    async with state.proxy() as data:
        data["category_title"] = message.text
        await db.add_category(data["category_title"])
    
    await state.finish()
    await message.answer("Категория успешно добавлена", reply_markup=user.reply_keyboard)

async def add_question_command_handler(message: types.Message):
    """ Обработчик комманды /add_question
        Начало ввода данных для добавления вопроса
    """
    # Устанавливаем ожидание ввода названия категории
    await QuestionAddFSM.category_title.set()
    # Показываем клавиатуру для выбора категории
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    categories = await db.fetch_all_categories()
    user.generate_categories_keyboard_buttons(markup, categories)
    markup.add(KeyboardButton("Отмена"))

    await message.answer("Выберите категорию для добавления вопроса:", reply_markup=markup)

async def add_question_category_title_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее название категории """
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Отмена"))
    
    async with state.proxy() as data:
        # Сохраняем данные в оперативной памяти (с помощью специального объекта)
        data["question_category_title"] = message.text
    # Устанавливаем ожидание ввода следующего поля класса QuestionAddFSM (название вопроса)
    await QuestionAddFSM.next()
    await message.answer("Введите название вопроса:", reply_markup=markup)
    
async def add_question_title_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее название вопроса """
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Отмена"))
    
    async with state.proxy() as data:
        # Сохраняем данные в оперативной памяти (с помощью специального объекта)
        data["question_title"] = message.text

    # Устанавливаем ожидание ввода следующего поля класса QuestionAddFSM (описание вопроса)
    await QuestionAddFSM.next()
    await message.answer("Введите описание вопроса:", reply_markup=markup)

async def add_question_description_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее описание вопроса """
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("Отмена"))
    
    async with state.proxy() as data:
        # Сохраняем данные в оперативной памяти (с помощью специального объекта)
        data["question_description"] = message.text
        # Добавлям вопрос в базу данных
        await db.add_question(
            data["question_category_title"],
            data["question_title"],
            data["question_description"]
        )
        
    # Устанавливам конец ожидания ввода (ввод завершен)
    await state.finish()
    await message.answer("Вопрос успешно добавлен", reply_markup=user.reply_keyboard)

async def delete_category_command_handler(message: types.Message):
    """ Обработчик команды /delete_category """
    # Устанавливаем ожидание ввода названия категории
    await CategoryDeleteFSM.category_title.set()
    # Показываем клавиатуру для выбора категории, которую требуется удалить
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    categories = await db.fetch_all_categories()
    user.generate_categories_keyboard_buttons(markup, categories)
    markup.add(KeyboardButton("Отмена"))

    await message.answer("Выберите категорию, которую требуется удалить:", reply_markup=markup)

async def delete_category_title_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее название категории """
    async with state.proxy() as data:
        data["category_title"] = message.text
        await db.delete_category(data["category_title"])

    await state.finish()
    await message.answer("Категория успешно удалена", reply_markup=user.reply_keyboard)

async def delete_question_command_handler(message: types.Message):
    """ Обработчик команды /delete_question """
    # Устанавливаем ожидание ввода названия вопроса
    await QuestionDeleteFSM.question_title.set()
    # Показываем клавиатуру для выбора категории, которую требуется удалить
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    questions = await db.fetch_all_questions()
    user.generate_questions_keyboard_buttons(markup, questions)
    markup.add(KeyboardButton("Отмена"))

    await message.answer("Выберите вопрос, который требуется удалить:", reply_markup=markup)
    
async def delete_question_category_title_handler(message: types.Message, state: FSMContext):
    """ Обработчик сообщения содержащее название вопроса """
    async with state.proxy() as data:
        data["question_title"] = message.text
        await db.delete_question(data["question_title"])
    
    await state.finish()
    await message.answer("Вопрос успешно удален", reply_markup=user.reply_keyboard)

async def cancel_handler(message: types.Message, state: FSMContext):
    """ Обработчик отмены операции добавления """
    current_state = await state.get_state()
    if current_state == None:
        return
    await state.finish()
    await message.answer("Добавление отменено", reply_markup=user.reply_keyboard)

def register_handlers(dp: Dispatcher) -> None:
    """ Функция для регистрации всех обработчиков """
    dp.register_message_handler(cancel_handler, Text(equals="Отмена"), state="*")

    dp.register_message_handler(add_category_command_handler, commands="add_category", state=None)
    dp.register_message_handler(add_category_title_handler, state=CategoryAddFSM.category_title)

    dp.register_message_handler(add_question_command_handler, commands="add_question", state=None)
    dp.register_message_handler(add_question_category_title_handler, state=QuestionAddFSM.category_title)
    dp.register_message_handler(add_question_title_handler, state=QuestionAddFSM.question_title)
    dp.register_message_handler(add_question_description_handler, state=QuestionAddFSM.question_description)

    dp.register_message_handler(delete_category_command_handler, commands="delete_category", state=None)
    dp.register_message_handler(delete_category_title_handler, state=CategoryDeleteFSM.category_title)

    dp.register_message_handler(delete_question_command_handler, commands="delete_question", state=None)
    dp.register_message_handler(delete_question_category_title_handler, state=QuestionDeleteFSM.question_title)