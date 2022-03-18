# from saved_forms
# select form by id -> display -> add actiions
#                                  |   |         |
#                            rename  add_after  del
# + handler
# add after = choose menu + insert aft id (fsm) 
#
# end => display
#
# input: form_id, user_id

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot_elements.storages.all_storages import unique_form_id, temp_mem_for_form_creator
from bot_elements.forms.form_display import display_form, display_current_temp_mem_status
from bot_elements.setter.all_setters import mem_for_created_forms_set_new_question_name, temp_mem_for_form_creator_add_element, mem_for_created_forms_insert_element
from bot_elements.remover.all_removers import temp_mem_for_form_creator_remove_form
from bot_elements.getter.all_getters import temp_mem_for_form_creator_get_data


class newQuestionName(StatesGroup):
    """ FSM для изменения текста 1 вопроса формы"""
    # waiting_for_data = State()
    waiting_for_new_question_name = State()


class appendQuestion(StatesGroup):
    """ FSM для добавления одного вопроса/ опроса в форму"""

    waiting_for_question = State()
    waiting_for_options = State()


async def edit_form_menu(message: types.Message):
    """ Меню редактора формы"""
    form_id = int(message.text[6:])
    await display_form(form_id=form_id, message=message)


async def rename_question_begin(message: types.Message, state: FSMContext):
    """ (newQuestionName FSM) Берет индексы формы и вопроса из команды и спрашивает новый текст вопроса"""
    form_ids = message.text[7:].split('_')
    form_id = int(form_ids[0])
    question_id = int(form_ids[1])

    await state.update_data(form_id=form_id)
    await state.update_data(question_id=question_id)
    await message.answer('Введите измененный вопрос')
    await newQuestionName.waiting_for_new_question_name.set()


async def rename_question_end(message: types.Message, state: FSMContext): # newQuestionName.waiting_for_new_question_name
    """ (newQuestionName FSM) Меняет на новый текст вопроса"""
    new_question_name = message.text
    data = await state.get_data()
    mem_for_created_forms_set_new_question_name(form_id=data['form_id'], question_id=data['question_id'], new_question_name=new_question_name)
    await display_form(form_id=data['form_id'], message=message)
    await state.finish()


async def choose_type(message: types.Message, state: FSMContext):  
    """ (form FSM) Предлагает выбрать тип добавляемого вопроса"""
    form_ids = message.text[10:].split('_')

    form_id = int(form_ids[0])
    question_id = int(form_ids[1])

    await state.update_data(form_id=form_id)
    await state.update_data(question_id=question_id)

    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll_single"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg_single")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.reply("Выберите тип вопроса", reply_markup=keyboard)


async def get_question(message: types.Message, state: FSMContext): # form.waiting_for_question
    """ (form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""
    
    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':

        temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': data['question'], 'message_id': 0, 'type': 'msg'})
        
        mem_for_created_forms_insert_element(form_id=data['form_id'], inser_after_id=data['question_id'], data=temp_mem_for_form_creator_get_data(message.chat.id).copy())

        temp_mem_for_form_creator_remove_form(user_id=message.chat.id)
        # await display_current_temp_mem_status(message)

        await display_form(form_id=data['form_id'], message=message)
        await state.finish()

    else:
        await state.update_data(question=question)
        await message.reply('Пришлите варианты ответов через запятую')
        await appendQuestion.waiting_for_options.set()


async def get_options(message: types.Message, state: FSMContext): # form.waiting_for_options
    """ (form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

    options = message.text.split(',')
    await state.update_data(options=options)
    
    data = await state.get_data()
    # print(user_data['question'], user_data['options'])

    temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': data['question'], 'options': data['options'], 'message_id': 0, 'type': 'poll'})
    
    mem_for_created_forms_insert_element(form_id=data['form_id'], inser_after_id=data['question_id'], data=temp_mem_for_form_creator_get_data(message.chat.id).copy())

    temp_mem_for_form_creator_remove_form(user_id=message.chat.id)
    
    await display_form(form_id=data['form_id'], message=message)
    await state.finish()


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания опроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await appendQuestion.waiting_for_question.set()


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания обычного вопроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await appendQuestion.waiting_for_question.set()


def register_handlers_editor(dp: Dispatcher):
    dp.register_message_handler(
        edit_form_menu, lambda message: message.text.startswith('/edit_'))
    dp.register_message_handler(rename_question_begin, lambda message: message.text.startswith('/rename'))
    dp.register_message_handler(choose_type, lambda message: message.text.startswith('/add_after'))
    dp.register_message_handler(rename_question_end, state=newQuestionName.waiting_for_new_question_name)

    dp.register_message_handler(get_question, state=appendQuestion.waiting_for_question)
    dp.register_message_handler(get_options, state=appendQuestion.waiting_for_options)

    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll_single")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg_single")
