import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, types, executor
import aiogram
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.register_user import register_handlers_register
from app.handlers.common import register_handlers_common
# from app.handlers.create_poll import register_handlers

# from polls import cmd_poll


API_TOKEN = '5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
mem = []
# cring


@dp.message_handler(commands=["poll"])
async def cmd_poll(message: types.message):
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    chat_id = message.chat.id
    is_anonymous = True
    open_period = 10
    question = 'you are'
    global poll
    poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, open_period=open_period, question=question, chat_id=chat_id)
    mem.append(poll)


@dp.poll_handler()
async def handle_poll_answer(poll_answer: types.Poll):
    # ans = aiogram.types.update.Update.poll.options

    print(poll_answer)
    # await bot.stop_poll(poll.chat_id, poll.message_id)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/poll", description="Опрос"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():

    register_handlers_common(dp)
    register_handlers_register(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
