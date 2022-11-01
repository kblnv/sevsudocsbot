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


if __name__ == "__main__":
    main()