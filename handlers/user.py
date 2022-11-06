# Файл, содержащий пользовательские обработчики

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup

from keyboards import user
from database import db

async def questions_callback_handler(callback: types.CallbackQuery):
    (_, id) = callback.data.split('_')
    (id, title, text) = db.fetch_one_question(id)
    await callback.message.answer(text)
    await callback.answer()

async def start_handler(message: types.Message):
    """ Обработчик /start и /help """
    await message.answer("Старт работы бота!", reply_markup=user.ureply_keyboard)

# TODO Переписать функции вида Text(equals="Все вопросы"), Text(equals="Настройки")
async def echo_handler(message: types.Message):
    """ Обработчик остальных сообщений """
    if (message.text == "Все вопросы 📄"):
        markup = InlineKeyboardMarkup(row_width=1)
        questions = db.fetch_all_questions()
        user.generate_inline_buttons(markup, questions)
        await message.answer("Список всех вопросов:", reply_markup=markup)
    elif (message.text == "Настройки ⚙️"):
        await message.answer(message.text)

def register_handlers(dp: Dispatcher) -> None:
    """ Функция для регистрации всех обработчиков """
    dp.register_callback_query_handler(
        questions_callback_handler,
        lambda callback: callback.data.startswith("btn_")
    )
    dp.register_message_handler(start_handler, commands=["start", "help"])
    dp.register_message_handler(echo_handler)