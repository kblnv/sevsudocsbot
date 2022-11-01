# Файл, содержащий пользовательские обработчики

from aiogram import Dispatcher, types


async def start_handler(message: types.Message):
    """ Обработчик /start и /help """
    await message.answer("Старт работы бота!")

async def echo_handler(message: types.Message):
    """ Обработчик остальных сообщений """
    await message.answer(message.text)

def register_handlers(dp: Dispatcher):
    """ Функция для регистрации всех обработчиков """
    dp.register_message_handler(start_handler, commands=["start", "help"])
    dp.register_message_handler(echo_handler)


# Аналогично определениям:
# @dp.message_handler(commands=["start", "help"])
# async def start_handler(message: types.Message):
#     """ Обработчик /start и /help """
#     await message.answer("Старт работы бота!")

# @dp.message_handler()
# async def echo_handler(message: types.Message):
#     """ Обработчик остальных сообщений """
#     await message.answer(message.text)
