# Файл, содержащий пользовательские обработчики

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text, Filter
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from keyboards import user
from database import db

class IsCategory(Filter):
    """ Кастомный фильтр
        Определяет, является ли сообщение названием категории
    """
    async def check(self, message: types.Message):
        categories = await db.fetch_all_categories()

        for (_, title) in categories:
            if title == message.text:
                return True

        return False

async def back_command_handler(message: types.Message):
    await message.answer(message.text, reply_markup=user.reply_keyboard) 

async def questions_callback_handler(callback: types.CallbackQuery):
    """ Обработчик нажатия на инлайн кнопку """
    (_, id) = callback.data.split('_')
    (_, _, _, description) = await db.fetch_one_question_by_id(id)
    await callback.message.answer(description)
    await callback.answer()

async def start_command_handler(message: types.Message):
    """ Обработчик команд /start и /help """
    await message.answer("Старт работы бота!", reply_markup=user.reply_keyboard)

async def all_categories_command_handler(message: types.Message):
    """ Обработчик команды "Категории" """
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    categories = await db.fetch_all_categories()
    user.generate_categories_keyboard_buttons(markup, categories)
    markup.add(KeyboardButton("Назад"))

    if len(categories) > 0:
        await message.answer(message.text, reply_markup=markup)
    else:
        await message.answer("Нет категорий")

async def one_category_command_handler(message: types.Message):
    """ Обработчик нажатия на конкретную категорию """
    markup = InlineKeyboardMarkup(row_width=1)
    questions = await db.fetch_all_questions_by_category_title(message.text)
    user.generate_inline_buttons(markup, questions)
    if (len(questions) > 0):
        await message.answer("Выберите интересующий вопрос:", reply_markup=markup)
    else:
        await message.answer("К данной категории не относится ни одного вопроса")

async def settings_command_handler(message: types.Message):
    """ Обработчик кнопки меню "Настройки" """
    await message.answer(message.text)

def register_handlers(dp: Dispatcher) -> None:
    """ Функция для регистрации всех обработчиков """
    dp.bind_filter(IsCategory)  # Регистрация кастомного фильтра

    dp.register_callback_query_handler(
        questions_callback_handler,
        lambda callback: callback.data.startswith("btn_")
    )
    dp.register_message_handler(start_command_handler, commands=["start", "help"])
    dp.register_message_handler(all_categories_command_handler, Text(equals="Категории"))
    dp.register_message_handler(one_category_command_handler, IsCategory())
    dp.register_message_handler(settings_command_handler, Text(equals="Настройки"))
    dp.register_message_handler(back_command_handler, Text(equals="Назад"))