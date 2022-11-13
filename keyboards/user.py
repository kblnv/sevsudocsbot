from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def generate_inline_buttons(markup: InlineKeyboardMarkup, questions: list) -> None:
    """ Функция генерации кнопок вопросов каждой категории"""
    for (id, _, title, _) in questions:
        markup.add(
            InlineKeyboardButton(text=title, callback_data="btn_" + str(id))
        )

def generate_keyboard_buttons(markup: ReplyKeyboardMarkup, categories: list) -> None:
    """ Функия генерации кнопок категорий """
    for (_, title) in categories:
        markup.add(KeyboardButton(text=title))


# Клавиатура
reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

all_questions_btn = KeyboardButton(text="Категории")
settings_btn = KeyboardButton(text="Настройки")

reply_keyboard.add(all_questions_btn, settings_btn)

