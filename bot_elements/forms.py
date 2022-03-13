""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


unique_form_id = 0

temp_form_recipient_data = {} # {'*form_creator_user_id*': {recip data}}
temp_mem_for_form_creator = {} # {'*form_creator_user_id*': [form data], ...}

mem_for_created_forms = {} # {*form_id*: {'form_data': [form data]}, ...}
send_forms_mem = [] # ['form_id': {'form_creator_user_id': id,'send_to_users_id': [ids]}, ... ]

# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem

forms_dispatcher = []

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')


async def display_current_temp_mem_status(message: types.Message):
    form_mem = temp_mem_for_form_creator[message.chat.id]
    print('form_mem ', form_mem)
    recip_mem = temp_form_recipient_data[message.chat.id]
    print('recip_mem ', recip_mem)
    parsed_msg = "name: " + recip_mem['form_name'] + ' '+ 'form_id: ' + str(recip_mem['form_id']) + "\n"
    if form_mem:
        question_number = 0
        for inside_mem in form_mem:
            if inside_mem['type'] == 'poll':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                    str(e) for e in inside_mem['options']) + ']' + ' ' + '/del' + str(question_number) + '\n')

            elif inside_mem['type'] == 'msg':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] +
                                  ' ' + '/del' + str(question_number) + '\n')

            question_number += 1

        await message.answer(parsed_msg)


class name(StatesGroup):
    """ FSM для выбора названия опроса"""
    waiting_for_name = State()


class form(StatesGroup):
    """ FSM для добавления одного вопроса/ опроса в форму"""

    waiting_for_question = State()
    waiting_for_options = State()


async def choose_name(message: types.Message, state: FSMContext):
    """ Предлагает выбрать название формы"""

    await message.reply("Выберите название формы")
    await name.waiting_for_name.set()


async def choose_type(message: types.Message, state: FSMContext):  # name.waiting_for_name
    """ Запоминает название и предлагает выбрать тип первого добавляемого вопроса"""
    global unique_form_id

    if not message.chat.id in temp_form_recipient_data:
        temp_form_recipient_data[message.chat.id] = {}

    temp_form_recipient_data[message.chat.id]["form_name"] = str(message.text)
    temp_form_recipient_data[message.chat.id]["type"] = "info"
    temp_form_recipient_data[message.chat.id]["form_id"] = unique_form_id
    temp_form_recipient_data[message.chat.id]["creator_id"] = message.chat.id
    unique_form_id += 1

    # temp_form_recipient_data["form_name"] = str(message.text)
    # temp_form_recipient_data["type"] = "info"

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
    """ Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""

    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':
        print('temp_mem_for_form_creator', temp_mem_for_form_creator)
        if message.chat.id in temp_mem_for_form_creator:
            temp_mem_for_form_creator[message.chat.id].append(
                {'question': data['question'], 'message_id': 0, 'type': 'msg'})
        else:
            temp_mem_for_form_creator[message.chat.id] = [
                {'question': data['question'], 'message_id': 0, 'type': 'msg'}]
        print('temp_mem_for_form_creator', temp_mem_for_form_creator)
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
        
        await state.finish()

    else:
        await state.update_data(question=question)
        await message.reply('Пришлите варианты ответов через запятую')
        await form.waiting_for_options.set()


async def get_options(message: types.Message, state: FSMContext):
    """ Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

    options = message.text.split(',')
    await state.update_data(options=options)

    user_data = await state.get_data()
    # print(user_data['question'], user_data['options'])

    print('temp_mem_for_form_creator', temp_mem_for_form_creator)
    if message.chat.id in temp_mem_for_form_creator:
        temp_mem_for_form_creator[message.chat.id].append(
            {'question': user_data['question'], 'options': user_data['options'], 'message_id': 0, 'type': 'poll'})
    else:
        temp_mem_for_form_creator[message.chat.id] = [
            {'question': user_data['question'], 'options': user_data['options'], 'message_id': 0, 'type': 'poll'}]
    print('temp_mem_for_form_creator', temp_mem_for_form_creator)

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
    """ Выбор параметров для нового вопроса"""

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
    """ Заканчивает создание формы"""
    
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await display_current_temp_mem_status(call.message)

    if call.message.chat.id in temp_mem_for_form_creator:
        temp_mem_for_form_creator[call.message.chat.id].append(
            temp_form_recipient_data[call.message.chat.id].copy())
    else:
        temp_mem_for_form_creator[call.message.chat.id] = [
            temp_form_recipient_data[call.message.chat.id].copy()]

    mem_for_created_forms[temp_form_recipient_data[call.message.chat.id]['form_id']] = (temp_mem_for_form_creator[call.message.chat.id].copy())
    
    print('mem_for_created_forms ', mem_for_created_forms)
    
    temp_mem_for_form_creator.pop(call.message.chat.id, None)
    temp_form_recipient_data.pop(call.message.chat.id, None)
    print('temp_form_recipient_data ', temp_form_recipient_data)
    
    await call.message.answer('Форма создана')


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания опроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос')
    await form.waiting_for_question.set()


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания обычного вопроса"""
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос')
    await form.waiting_for_question.set()

'''
async def activate_cycle(message: types.Message):
    """ Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""

    form_name = str(message.text)[6:]
    curr_form = {}
    curr_form['user_id'] = message.chat.id
    curr_form['form_name'] = form_name
    forms_dispatcher.append(curr_form.copy())
    curr_form.clear()

    await go_cycle()


# complete polls
async def go_cycle():
    """Отсылает вопросы/ опросы из forms_dispatcher"""

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

                    elif curr_quest['type'] == 'info':
                        multiple_polls_dispatcher[0].remove(
                            {'form_name': curr_quest['form_name'], 'user_id': curr_quest['user_id'], 'type': 'info'})
                        multiple_polls_dispatcher.pop(0)
                        forms_dispatcher.remove(
                            {'user_id': curr_started_form['user_id'], 'form_name': form_name})
                        print('theend')


def lambda_checker_poll(poll):
    """Проверяет принадлежит ли опрос выбранной форме"""

    for data in multiple_polls_dispatcher:
        for a in data:
            # print(a)
            if a['id'] == poll['id']:
                data.remove(
                    {'question': a['question'], 'options': a['options'], 'id': a['id'], 'type': 'poll'})
                # print('eh')
                return True
    # print('folss')
    return False


def lambda_checker_msg(message: types.Message):
    """Проверяет является ли сообщение ответом на вопрос из формы"""

    for data in multiple_polls_dispatcher:
        for a in data:
            # ! проверить, не совпадают ли айдишники из разных чатов
            if a['id'] + 1 == message.message_id:
                data.remove(
                    {'question': a['question'], 'id': a['id'], 'type': 'msg'})
                # print('eh')
                # print(message.text)
                return True
    # print('folss')
    return False


# handler activates when vote/send answer
async def poll_handler(poll: types.PollAnswer):
    """Активируется, когда приходит ответ на опрос/ опрос закрывается"""

    print(poll)
    if multiple_polls_dispatcher:
        print('go ahead pol')
        await go_cycle()
    # print(poll['id'])


async def msg_handlr(message: types.Message):
    """Активируется, когда приходит сообщение"""

    print(message)
    if multiple_polls_dispatcher:
        # print('go ahead msg')
        await go_cycle()
'''

async def del_handler(message: types.Message):
    """Удаляет одну запись из списка temp_mem по её идентификатору"""

    delete_id = int(message.text[4:])
    temp_mem_for_form_creator[message.chat.id].pop(delete_id)
    await message.answer('удалил пункт ' + str(delete_id))
    await display_current_temp_mem_status(message)

def register_handlers_forms(dp: Dispatcher):
    dp.register_message_handler(choose_name, commands="multi_form", state="*")

    dp.register_message_handler(choose_type, state=name.waiting_for_name)
    dp.register_message_handler(get_question, state=form.waiting_for_question)
    dp.register_message_handler(get_options, state=form.waiting_for_options)
    # dp.register_message_handler(activate_cycle, commands='send')

    dp.register_callback_query_handler(
        add_quest_true, text="add_quest_true")
    dp.register_callback_query_handler(
        add_quest_false, text="add_quest_false")
    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg")

    dp.register_message_handler(
        del_handler, lambda message: message.text.startswith('/del'))
'''
    dp.register_poll_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
    dp.register_message_handler(
        msg_handlr, lambda message: lambda_checker_msg(message))
'''
    

