import asyncio
import time
from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from register import register_handlers_register
from forms import register_handlers_forms

import full_pars_2


rasp = full_pars_2.parse_group_today('М3О-221Б-20')

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def rasp_notification():
    while True:

        #  rasp = full_pars_2.parse_group_today('М3О-221Б-20') - ЗАПИХНИ ЭТО В САМОЕ НАЯАЛО ПЕРЕД ВСЕМИ ФУНКЦИЯМИ

        await asyncio.sleep(1)
        for data in rasp:
            time_diff = -(int(time.localtime().tm_hour) * 60 + int(time.localtime().tm_min)) + \
                int(data['time_start_hour']) * 60 + \
                int(data['time_start_minutes'])
            if time_diff <= 15 and time_diff > 0:
                pass
                # for user in data['notify']:
                #     if int(user['notify_status']) != 1:
                #         await bot.send_message(user['user'], str(data['name']) + ' через {0} минут'.format(time_diff))
                #         user['notify_status'] = 1
            # print(time_diff, data['name'])

if __name__ == '__main__':
    bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')
    dp = Dispatcher(bot, storage=MemoryStorage(), loop=asyncio.get_event_loop())
    dp.loop.create_task(set_commands(bot))
    dp.loop.create_task(rasp_notification())
    register_handlers_forms(dp)
    register_handlers_register(dp)
    executor.start_polling(dp)
