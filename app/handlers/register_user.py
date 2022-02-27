from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sys
sys.path.append('C:\\Users\\ИЛЮХА-БОСС\\Desktop\\Прога\\Python\\telegram_bot\\db_setting')
import tg_connect_db as tg_db


class registerUser(StatesGroup):
    waiting_for_group = State()
    waiting_for_fio = State()


async def register_start(message: types.Message):
    await message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()



async def fio_choosen(message: types.Message, state: FSMContext):
    fio = message.text.lower()
    if not fio:
        await message.answer("Введите корректные ФИО")
        return
    await message.answer('your fio:' + fio)
    await state.update_data(chosen_fio=fio)
    await registerUser.next()
    await message.answer('Выберите группу')
    await registerUser.waiting_for_group.set()


async def group_chosen(message: types.Message, state: FSMContext):
    group = message.text.lower()

    if not group:
        await message.answer("Введите корректную группу")
        return
    await message.answer('your group: ' + group)
    await state.update_data(chosen_group=group)
    
    user_data = await state.get_data()
    await message.answer(f"Ваша группа: {user_data['chosen_group']}.\n")
    await message.answer(f"Ваши ФИО: {user_data['chosen_fio']}.\n")
    await message.answer(f"Ваш ID: {message.from_user.id}")

    tg_db.reg_us(user_data['chosen_fio'], message.from_user.id, 'stud' ,group_stud = user_data['chosen_group'])

    # выбранную группу можно взять с помощью user_data['chosen_group']

    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_start, commands="register", state="*")
    dp.register_message_handler(fio_choosen, state=registerUser.waiting_for_fio)
    dp.register_message_handler(group_chosen, state=registerUser.waiting_for_group)
