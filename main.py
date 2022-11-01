# Файл - точка входа бота

from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, executor

import config
from handlers import user


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Включение логирования
basicConfig(level=INFO)


async def on_startup(_):
    """ Функция, срабатывающая при старте бота """
    pass

def main():
    """ Точка входа """
    user.register_handlers(dp)  # Включаем обработчики из файла user
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

button_hi = KeyboardButton('Здарова, очередняра! 👋', callback_data='buttonhi')

Arthas = InlineKeyboardMarkup().add(InlineKeyboardButton("Плюс мораль", url="https://www.youtube.com/c/SpitefulDick"))
set_button_inline = InlineKeyboardMarkup().add(button_hi)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!", reply_markup = set_button_inline)

@dp.callback_query_handler(lambda c: c.data == 'buttonhi')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Ротик закрыт, а животик то урчит...', reply_markup = Arthas)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.message_handler(commands=['zxc'])
async def process_zxc_command(msg):
    for i in range(1000,13,-7):
        await bot.send_message(msg.from_user.id, str(i) + " - 7 = " + str(i-7))
        await asyncio.sleep(0.2)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    
if __name__ == "__main__":
    main()
