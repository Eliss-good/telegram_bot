from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
import aiogram

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "/register для регистрации",
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")


# async def cmd_poll(message: types.Message):
    
#     await message.answer('Высылаю опрос')
#     options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
#     chat_id = '@KremlynBot'
#     is_anonymous = True
#     open_period = 60
#     question = 'you are'
#     result = await aiogram.methods.send_poll.SendPoll(options=options, is_anonymous=is_anonymous, open_period=open_period, question=question)
    
    


def register_handlers_common(dp: Dispatcher):
    # dp.register_message_handler(cmd_poll, commands="poll", state="*")
    # dp.register_poll_handler(cmd_poll)
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

