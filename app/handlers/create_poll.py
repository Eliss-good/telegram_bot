from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class registerPoll(StatesGroup):
    waiting_for_poll = State()


async def start(message: types.Message, state: FSMContext):
    await registerPoll.waiting_for_poll.set()
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    chat_id = '@KremlynBot'
    is_anonymous = True
    open_period = 60
    poll = await Bot.sendPoll(chat_id=chat_id, options=options, is_anonymous=is_anonymous, open_period=open_period)
    
    await state.finish()
    


# async def group_chosen(message: types.Message, state: FSMContext):
    
    
    
    # await state.update_data(chosen_group=group)
    # user_data = await state.get_data()
    # await message.answer(f"Ваша группа: {user_data['chosen_group']}.\n")

    # выбранную группу можно взять с помощью user_data['chosen_group']

    # await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="poll", state="*")
    dp.register_message_handler(
        start, state=registerPoll.waiting_for_poll)

