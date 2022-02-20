import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.register_user import register_handlers_register
from app.handlers.common import register_handlers_common


API_TOKEN = ''


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # config = load_config("config/bot.ini")
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_common(dp)
    register_handlers_register(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
