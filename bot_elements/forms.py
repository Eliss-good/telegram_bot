""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


unique_form_id = 0

temp_form_recipient_data = {} # {'*form_creator_user_id*': {recip data}}
temp_mem_for_form_creator = {} # {'*form_creator_user_id*': [form data], ...}

mem_for_created_forms = {} # {*form_id*: [form data], ...}
send_forms_mem = [] # [{'form_id': *form_id*, 'sent_form_id': *id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [ids]}, ... ]

# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher

completing_forms_dispatcher = {} # {'user_id': {''unique_form_id'': id, 'unique_sent_form_id': id, 'curr_page': num, 'form_copy': [form_data]}, ...}

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
    

