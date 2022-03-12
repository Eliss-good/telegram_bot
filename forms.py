""" Система опросов"""
from select import poll
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

poll_recipient_data = {}
temp_mem_for_multiple_poll = []
multiple_polls_dispatcher = []

forms_dispatcher = []

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')


async def display_current_temp_mem_status(message: types.Message):
    mem = temp_mem_for_multiple_poll
    parsed_msg = "name: " + poll_recipient_data['form_name'] + "\n"
    if mem:
        question_number = 0
        for inside_mem in mem:
            if inside_mem['type'] == 'poll':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                    str(e) for e in inside_mem['options']) + ']' + ' ' + '/del' + str(question_number) + '\n')

            elif inside_mem['type'] == 'msg':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] +
                                  ' ' + '/del' + str(question_number) + '\n')

            question_number += 1

        await message.answer(parsed_msg)


class nameAndQuestionType(StatesGroup):
    waiting_for_name = State()

# poll create fsm
class form(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()


async def choose_name(message: types.Message, state: FSMContext):
    await message.reply("Выберите название формы")
    await nameAndQuestionType.waiting_for_name.set()


async def choose_question(message: types.Message, state: FSMContext):
    poll_recipient_data["form_name"] = str(message.text)
    poll_recipient_data["user_id"] = 506629389
    poll_recipient_data["type"] = "recipient_info"

    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    
    await message.reply("Выберите тип вопроса", reply_markup=keyboard)
    await state.finish()


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
                text="Нет", callback_data="add_quest_false")

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await display_current_temp_mem_status(message)

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
            text="Нет", callback_data="add_quest_false")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await display_current_temp_mem_status(message)

    await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    # print(temp_mem_for_multiple_poll)
    await state.finish()


# callback queries handlers

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
    await display_current_temp_mem_status(call.message)
    temp_mem_for_multiple_poll.append(poll_recipient_data.copy())
    
    poll_recipient_data.clear()
    multiple_polls_dispatcher.append(temp_mem_for_multiple_poll.copy())
    temp_mem_for_multiple_poll.clear()
    print(multiple_polls_dispatcher)
    await call.message.answer('Форма создана')


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос')
    await form.waiting_for_question.set()


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос')
    await form.waiting_for_question.set()


async def activate_cycle(message: types.Message):
    form_name = str(message.text)[6:]
    curr_form = {}
    curr_form['user_id'] = message.from_user.id
    curr_form['form_name'] = form_name
    forms_dispatcher.append(curr_form.copy())
    curr_form.clear()
    await go_cycle()


# complete polls
async def go_cycle():
    print(forms_dispatcher)
    for curr_started_form in forms_dispatcher:
        form_name = curr_started_form['form_name']
        if multiple_polls_dispatcher:
            for select_form in multiple_polls_dispatcher:
                if select_form[-1]['form_name'] == form_name:

                    curr_quest = select_form[0]

                    if curr_quest['type'] == 'poll':

                        msg = await bot.send_poll(chat_id=curr_started_form['user_id'], question=curr_quest['question'], options=curr_quest['options'], is_anonymous=True)
                        curr_quest['id'] = msg.poll.id

                    elif curr_quest['type'] == 'msg':
                        msg = await bot.send_message(chat_id=curr_started_form['user_id'], text=curr_quest['question'])
                        curr_quest['id'] = msg.message_id
                        # print(curr_quest['id'])
                        
                    elif curr_quest['type'] == 'recipient_info':
                        multiple_polls_dispatcher[0].remove(
                            {'form_name': curr_quest['form_name'], 'user_id': curr_quest['user_id'], 'type': 'recipient_info'})
                        multiple_polls_dispatcher.pop(0)
                        forms_dispatcher.remove({'user_id': curr_started_form['user_id'], 'form_name': form_name})
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
    print('im her')
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


# handler activates when vote/send answer
async def poll_handler(poll: types.PollAnswer):
    print(poll)
    if multiple_polls_dispatcher:
        print('go ahead pol')
        await go_cycle()
    # print(poll['id'])


async def msg_handlr(message: types.Message):
    print(message)
    if multiple_polls_dispatcher:
        print('go ahead msg')
        await go_cycle()


async def del_handler(message: types.Message):
    """Удаляет одну запись из списка temp_mem по её идентификатору"""
    delete_id = int(message.text[4:])
    temp_mem_for_multiple_poll.pop(delete_id)
    await message.answer('удалил пункт ' + str(delete_id))


def register_handlers_forms(dp: Dispatcher):
    dp.register_message_handler(choose_name, commands="multi_form", state="*")

    dp.register_message_handler(choose_question, state=nameAndQuestionType.waiting_for_name)
    dp.register_message_handler(get_question, state=form.waiting_for_question)
    dp.register_message_handler(get_options, state=form.waiting_for_options)
    dp.register_message_handler(activate_cycle, commands='send')

    dp.register_callback_query_handler(
        add_quest_true, text="add_quest_true")
    dp.register_callback_query_handler(
        add_quest_false, text="add_quest_false")
    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg")

    dp.register_poll_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
    dp.register_message_handler(
        msg_handlr, lambda message: lambda_checker_msg(message))
    dp.register_message_handler(
        del_handler, lambda message: message.text.startswith('/del'))
