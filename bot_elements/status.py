""" Статус пользователя"""
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


# нужно доставать данные о фио, роли, группе, непройденных опросах, рейтинге из бд
from bot_elements.forms import send_forms_mem, mem_for_created_forms
from bot_elements.forms import completing_forms_dispatcher

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')


async def display_user_status(message: types.Message):
    full_message = "Полученные формы:"
    for select_form in send_forms_mem:
        if message.chat.id in select_form['info']['send_to_users_ids']:
            full_message += '\n' + str(mem_for_created_forms[select_form['form_id']][-1]['form_name']) + ' от пользователя ' + str(
                mem_for_created_forms[select_form['form_id']][-1]['creator_id']) + ' /complete_' + str(select_form['form_id']) + '_' + str(select_form['sent_form_id'])

    await message.answer(full_message)


async def complete_form(message: types.Message):
    form_indexes = message.text[10:].split('_')
    unique_form_id = int(form_indexes[0])
    unique_sent_form_id = int(form_indexes[1])
    completing_forms_dispatcher[message.chat.id] = {
        'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id}


async def activate_cycle(message: types.Message, unique_form_id, unique_sent_form_id):
    """ Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""
    await go_cycle()


# complete polls
async def go_cycle(unique_form_id, unique_sent_form_id):
    """Отсылает вопросы/ опросы из send_forms_mem при вызове"""

    select_form = mem_for_created_forms[unique_form_id]['form_data']
    curr_quest = select_form[0]

    chat_id = list(completing_forms_dispatcher.keys())[list(completing_forms_dispatcher.values(
    )).index({'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id})]

    if curr_quest['type'] == 'poll':

        msg = await bot.send_poll(chat_id=chat_id, question=curr_quest['question'], options=curr_quest['options'], is_anonymous=True)
        curr_quest['id'] = msg.poll.id

    elif curr_quest['type'] == 'msg':
        msg = await bot.send_message(chat_id=chat_id, text=curr_quest['question'])
        curr_quest['id'] = msg.message_id
# ! problem - need to change send forms
    elif curr_quest['type'] == 'info':
        completing_forms_dispatcher.remove(
            {'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id})

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


def register_handlers_status(dp: Dispatcher):
    dp.register_message_handler(
        display_user_status, commands="status", state="*")
    dp.register_message_handler(
        complete_form, lambda message: message.text.startswith('/complete'))
