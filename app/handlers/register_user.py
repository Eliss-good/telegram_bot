from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class registerUser(StatesGroup):
    waiting_for_fio = State()
    waiting_for_group = State()


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


async def group_chosen(message: types.Message, state: FSMContext):
    group = message.text
    if not group:
        await message.answer("Введите корректную группу")
        return
    user_data = await state.get_data()
    await message.answer(f"Ваша группа {message.text.lower()}, {user_data['chosen_fio']}.\n")
    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_start, commands="register", state="*")
    dp.register_message_handler(
        fio_choosen, state=registerUser.waiting_for_fio)
    dp.register_message_handler(
        group_chosen, state=registerUser.waiting_for_group)
