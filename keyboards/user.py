from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def generate_inline_buttons(markup: InlineKeyboardMarkup, questions: list) -> None:
    """ Функция генерации inline кнопок из информации с БД """
    for (id, title, _) in questions:
        markup.add(
            InlineKeyboardButton(text=title, callback_data="btn_" + str(id))
        )

# Клавиатура
ureply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

all_questions_btn = KeyboardButton(text="Все вопросы 📄")
settings_btn = KeyboardButton(text="Настройки ⚙️")

ureply_keyboard.add(all_questions_btn, settings_btn)

