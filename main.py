from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

kb = [
        [
            KeyboardButton(text="Размер стипендий🙈"),
            KeyboardButton(text="Стоимость аренды в общежитиях🙉"),
            KeyboardButton(text="Цена на хлеб 'Прибрежный' в Фрэше🙊"),
            KeyboardButton(text="Папич"),
            KeyboardButton(text="➡")
        ],
        [
            KeyboardButton(text="⬅")
        ],
    ]

kb_inline = [
        [
            InlineKeyboardButton(text="Артас, его величество",
                                 url="https://www.youtube.com/c/SpitefulDick"),
            InlineKeyboardButton(text="Лучшее с папичем",
                                 url="https://www.youtube.com/c/%D0%9B%D1%83%D1%87%D1%88%D0%B5%D0%B5%D1%81%D0%9F%D0%B0%D0%BF%D0%B8%D1%87%D0%B5%D0%BC"),
            InlineKeyboardButton(text="Рофланы Папича",
                                 url="https://www.youtube.com/c/%D0%A0%D0%BE%D1%84%D0%BB%D0%B0%D0%BD%D1%8B%D0%9F%D0%B0%D0%BF%D0%B8%D1%87%D0%B0/featured")
        ],
    ]

keyboard_reply_first = ReplyKeyboardMarkup(resize_keyboard=True).add(kb[0][0]).\
                                                                 add(kb[0][1]).\
                                                                 add(kb[0][2]).\
                                                                 add(kb[0][3]).\
                                                                 add(kb[0][4])
keyboard_reply_second = ReplyKeyboardMarkup(resize_keyboard=True).add(kb[1][0])

keyboard_inline_first = InlineKeyboardMarkup(resize_keyboard=True).add(kb_inline[0][0]).\
                                                                   add(kb_inline[0][1]).\
                                                                   add(kb_inline[0][2])
