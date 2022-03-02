import asyncio
from aiogram import Dispatcher, types, Bot

from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text

API_TOKEN = '5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
polls_dispcatcher = []


# ################regiser zone #############################

class registerUser(StatesGroup):
    waiting_for_role = State()
    waiting_for_fio = State()
    waiting_for_group = State()



@dp.message_handler(commands='register')
async def choose_role(message: types.Message):
    
    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="is_student"),
        types.InlineKeyboardButton(
            text="Преподаватель", callback_data="is_prepod")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите роль      ", reply_markup=keyboard)
    

@dp.message_handler(state=registerUser.waiting_for_fio)
async def fio_choosen(message: types.Message, state: FSMContext):
    fio = message.text.lower()
    await message.answer('your fio:' + fio)
    await state.update_data(chosen_fio=fio)
    user_data = await state.get_data()
    if user_data['chosen_role'] == 'student':
        await registerUser.next()
        await message.answer('Выберите группу')
    else:
        await message.reply('вы ' + user_data['chosen_fio'] + ' ' + user_data['chosen_role'])
        state.finish()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=registerUser.waiting_for_group)
async def choose_group(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['chosen_role'] != "prepod":
        await state.update_data(chosen_group=message.text)
        user_data = await state.get_data()
        await message.answer(f"{user_data['chosen_role']} {user_data['chosen_group']} {user_data['chosen_fio']}.\n")
    
    await state.finish()

@dp.callback_query_handler(text="is_student")
async def is_stud(call: types.CallbackQuery, state: FSMContext):
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="student")
    await call.answer()
    await registerUser.next()
    await call.message.answer('Введите ФИО')


@dp.callback_query_handler(text="is_prepod")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="prepod")
    await call.answer()
    user_data = await state.get_data()
    # await call.message.answer('Вы '+ user_data['chosen_role'])
    await registerUser.next()
    await call.message.answer('Введите ФИО')
    
# ################ tnd register ########

@dp.message_handler(commands=["poll"])
async def cmd_poll(message: types.message):
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    chat_id = message.chat.id
    is_anonymous = True
    # open_period = 10
    question = 'you are'
    global poll
    poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, question=question, chat_id=chat_id)
    
    # send chat id and poll id 
    polls_dispcatcher.append({"chat_id": poll.chat.id, "message_id": poll.message_id})
    await asyncio.sleep(5)
    count = 0
    for data in polls_dispcatcher:
        
        res = await bot.stop_poll(chat_id=data['chat_id'], message_id=data['message_id'])
        print(count, '  ', res)
        count += 1
    polls_dispcatcher.clear()
    count = 0




async def set_commands(bot: Bot):
    commands = [
        
        BotCommand(command="/poll", description="Опрос"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():



    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
