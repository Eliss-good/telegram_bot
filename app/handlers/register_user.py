from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class registerUser(StatesGroup):
    waiting_for_group = State()


async def register_start(message: types.Message):
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

    # выбранную группу можно взять с помощью user_data['chosen_group']

    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_start, commands="register", state="*")
    dp.register_message_handler(
        group_chosen, state=registerUser.waiting_for_group)
