# Файл - точка входа бота

from logging import basicConfig, INFO
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from handlers import user, admin
from database import db


mem_storage = MemoryStorage()

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=mem_storage)


# Включение логирования
basicConfig(level=INFO)


async def on_startup(_) -> None:
    """ Функция, срабатывающая при старте бота """
    await db.init()

async def on_shutdown(_) -> None:
    """ Функция, срабатывающая при завершении бота """
    await db.cur.close()
    await db.con.close()

def main() -> None:
    """ Точка входа """
    user.register_handlers(dp)  # Регистрируем обработчики из файла user
    admin.register_handlers(dp)  # Регистрируем обработчики из файла admin
    executor.start_polling(
        dp, skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown)


if __name__ == "__main__":
    main()