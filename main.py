# Файл - точка входа бота

from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, executor

import config
from handlers import user
from database import db


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Включение логирования
basicConfig(level=INFO)


async def on_startup(_) -> None:
    """ Функция, срабатывающая при старте бота """
    db.init()

async def on_shutdown(_) -> None:
    """ Функция, срабатывающая при завершении бота """
    db.con.close()


def main() -> None:
    """ Точка входа """
    user.register_handlers(dp)  # Регистрируем обработчики из файла user
    executor.start_polling(
        dp, skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown)


if __name__ == "__main__":
    main()