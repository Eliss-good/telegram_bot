import asyncio
import bot_elements.raspisanie.raspisanie as raspisanie
from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot_elements.register.register_for_prepod import register_handlers_register_prepod
from bot_elements.forms.forms import register_handlers_forms
from bot_elements.forms.forms_menu import register_handlers_forms_menu

from bot_elements.forms.forms_editor import register_handlers_forms_editor
from bot_elements.cancel import register_handlers_cancel


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/saved_forms",
                   description="Посмотреть сохраненные формы"),
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
    
    register_handlers_forms_editor(dp)
    register_handlers_forms(dp)
    register_handlers_forms_menu(dp)
    
    register_handlers_register_prepod(dp)
    executor.start_polling(dp)