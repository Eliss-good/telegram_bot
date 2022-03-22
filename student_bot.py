import asyncio
import bot_elements.raspisanie.raspisanie as raspisanie
from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_elements.register.register_for_student import register_handlers_register_student
from bot_elements.status.status import register_handlers_status
from bot_elements.cancel import register_handlers_cancel


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/status", description="Полученные формы"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    bot = Bot(token='')
    dp = Dispatcher(bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())
    dp.loop.create_task(set_commands(bot))
    dp.loop.create_task(raspisanie.rasp_notification('М3О-221Б-20'))
    
    register_handlers_cancel(dp)
    
    
    register_handlers_status(dp)
    
    register_handlers_register_student(dp)
    executor.start_polling(dp)
