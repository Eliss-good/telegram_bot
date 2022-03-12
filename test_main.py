import asyncio
import time
import raspisanie
from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from register import register_handlers_register
from forms import register_handlers_forms


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')
    dp = Dispatcher(bot, storage=MemoryStorage(), loop=asyncio.get_event_loop())
    dp.loop.create_task(set_commands(bot))
    dp.loop.create_task(raspisanie.rasp_notification('М3О-221Б-20'))
    register_handlers_forms(dp)
    register_handlers_register(dp)
    executor.start_polling(dp)
