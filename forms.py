""" Система опросов"""
from email.message import Message
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


temp_mem_for_multiple_poll = []

multiple_polls_dispatcher = []

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')

class form(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()


class group_chooser(StatesGroup):
    waiting_for_group = State()


async def choose_question(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.reply("Выберите тип вопроса", reply_markup=keyboard)


async def get_question(message: types.Message, state: FSMContext):

    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':
        temp_mem_for_multiple_poll.append(
            {'question': data['question'], 'id': 0, 'type': 'msg'})
        buttons = [
            types.InlineKeyboardButton(
                text="Да", callback_data="add_quest_true"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="add_quest_false"),
            types.InlineKeyboardButton(
                text="Удалить последний вопрос", callback_data="del_quest_true")
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
        # print(temp_mem_for_multiple_poll)
        await state.finish()

    else:
        await state.update_data(question=question)
        await message.reply('Пришлите варианты ответов через запятую')
        await form.waiting_for_options.set()


async def get_options(message: types.Message, state: FSMContext):

    options = message.text.split(',')
    await state.update_data(options=options)

    user_data = await state.get_data()
    # print(user_data['question'], user_data['options'])

    temp_mem_for_multiple_poll.append(
        {'question': user_data['question'], 'options': user_data['options'], 'id': 0, 'type': 'poll'})

    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false"),
        types.InlineKeyboardButton(
            text="Удалить последний вопрос", callback_data="del_quest_true")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    # print(temp_mem_for_multiple_poll)
    await state.finish()


async def choose_group(message: types.Message, state: FSMContext):

    group = message.text
    await message.answer('groop' + ' ' + group)
    # bd search
    users_id_list = [506629389]
    temp_mem_for_multiple_poll.append(
        {'users_id': users_id_list, 'type': 'recipient_info'})
    multiple_polls_dispatcher.append([*temp_mem_for_multiple_poll])

    # print(multiple_polls_dispatcher)
    temp_mem_for_multiple_poll.clear()
    await state.finish()


async def add_quest_true(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.reply('Выберите тип вопроса', reply_markup=keyboard)


async def add_quest_false(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('gotovo')

    await group_chooser.waiting_for_group.set()
    await call.message.answer('choose group')


async def del_quest_true(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    temp_mem_for_multiple_poll.pop()
    await call.message.answer('last quest deleted')
    # print(temp_mem_for_multiple_poll)
    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false"),
        types.InlineKeyboardButton(
            text="Удалить последний вопрос", callback_data="del_quest_true")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await form.waiting_for_question.set()
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос')


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await form.waiting_for_question.set()
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос')

async def activate_cycle(message: types.Message):
    await go_cycle()

async def go_cycle():
    print(multiple_polls_dispatcher)
    if multiple_polls_dispatcher:

        if multiple_polls_dispatcher[0]:

            if multiple_polls_dispatcher[0][0]:

                curr_quest = multiple_polls_dispatcher[0][0]
                for reciever in multiple_polls_dispatcher[0][-1]['users_id']:

                    # print(multiple_polls_dispatcher[0][-1]['users_id'])
                    if curr_quest['type'] == 'poll':

                        msg = await bot.send_poll(chat_id=506629389, question=curr_quest['question'], options=curr_quest['options'], is_anonymous=True)
                        curr_quest['id'] = msg.poll.id

                    elif curr_quest['type'] == 'msg':
                        msg = await bot.send_message(chat_id=reciever, text=curr_quest['question'])
                        curr_quest['id'] = msg.message_id
                        # print(curr_quest['id'])
                    else:
                        multiple_polls_dispatcher[0].remove(
                            {'users_id': curr_quest['users_id'], 'type': 'recipient_info'})
                        multiple_polls_dispatcher.pop(0)
                        print('theend')

def lambda_checker_poll(message):
    for data in multiple_polls_dispatcher:
        for a in data:
            # print(a)
            if a['id'] == message['id']:
                multiple_polls_dispatcher[0].remove(
                    {'question': a['question'], 'options': a['options'], 'id': a['id'], 'type': 'poll'})
                # print('eh')
                return True
    # print('folss')
    return False


def lambda_checker_msg(message: types.Message):
    for data in multiple_polls_dispatcher:
        for a in data:
            if a['id'] + 1 == message.message_id:
                multiple_polls_dispatcher[0].remove(
                    {'question': a['question'], 'id': a['id'], 'type': 'msg'})
                # print('eh')
                # print(message.text)
                return True
    # print('folss')
    return False


async def poll_handler(poll: types.PollAnswer):
    print(poll)
    if multiple_polls_dispatcher:
        await go_cycle()
    # print(poll['id'])


async def msg_handlr(message: types.Message):
    print(message)
    if multiple_polls_dispatcher:
        await go_cycle()


def register_handlers_forms(dp: Dispatcher):
    dp.register_message_handler(
        choose_question, commands="multi_form", state="*")
    dp.register_message_handler(get_question, state=form.waiting_for_question)
    dp.register_message_handler(get_options, state=form.waiting_for_options)
    dp.register_message_handler(choose_group, state=group_chooser.waiting_for_group)
    dp.register_message_handler(activate_cycle, commands='send')

    dp.register_callback_query_handler(
        add_quest_true, text="add_quest_true")
    dp.register_callback_query_handler(
        add_quest_false, text="add_quest_false")
    dp.register_callback_query_handler(
        del_quest_true, text="del_quest_true")
    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg")

    dp.register_poll_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
    dp.register_poll_handler(
        msg_handlr, lambda message: lambda_checker_msg(message))
