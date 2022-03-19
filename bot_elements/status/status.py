""" Статус пользователя"""
from aiogram import Bot, Dispatcher, types
from bot_elements.getter.all_getters import completing_forms_dispatcher_get_form_copy, mem_for_created_forms_get_creator_id, mem_for_created_forms_get_form_name
from bot_elements.remover.all_removers import completing_forms_dispatcher_remove_session

# нужно доставать данные о фио, роли, группе, непройденных опросах, рейтинге из бд
from bot_elements.storages.all_storages import send_forms_mem, completing_forms_dispatcher

from bot_elements.setter.all_setters import completing_forms_dispatcher_add_session

bot = Bot(token='5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ')


async def display_user_status(message: types.Message):
    print('xd')
    full_message = "Полученные формы:"
    print(send_forms_mem)
    for select_form in send_forms_mem:
        if message.chat.id in select_form['info']['send_to_users_ids']:
            
            full_message += '\n' + str(mem_for_created_forms_get_form_name(select_form['form_id'])) + ' от пользователя ' + str(mem_for_created_forms_get_creator_id(select_form['form_id'])) + ' /complete_' + str(select_form['form_id']) + '_' + str(select_form['sent_form_id'])

    await message.answer(full_message)


async def complete_form(message: types.Message):
    """ Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""

    form_indexes = message.text[10:].split('_')
    unique_form_id = int(form_indexes[0])
    unique_sent_form_id = int(form_indexes[1])

    completing_forms_dispatcher_add_session(chat_id=message.chat.id, unique_form_id=unique_form_id, unique_sent_form_id=unique_sent_form_id)

    print('completing_forms_dispatcher', completing_forms_dispatcher)
    await go_cycle(message=message, type='launch_from_message_handler')


# async def activate_cycle(unique_form_id, unique_sent_form_id):
#     """ Получает название формы, добавляет данные в forms_dispatcher,
#         запускает отправку вопросов из нужной формы"""
#     await go_cycle(unique_form_id, unique_sent_form_id)


# complete polls
async def go_cycle(message, type):
    """Отсылает вопросы/ опросы из send_forms_mem при вызове"""

    curr_question_num = 0

    user_id = 0
    if type == 'launch_from_poll_handler':
        print('i am nigger')
        user_id = message.user.id

    elif type == 'launch_from_message_handler':
        print('i am whiter')
        user_id = message.chat.id

    print(user_id)
    select_form = completing_forms_dispatcher_get_form_copy(user_id=user_id)

    curr_quest = select_form[curr_question_num]

    if curr_quest['type'] == 'poll':

        msg = await bot.send_poll(chat_id=user_id, question=curr_quest['question'], options=curr_quest['options'], is_anonymous=False)
        curr_quest['message_id'] = msg.poll.id

    elif curr_quest['type'] == 'msg':
        msg = await bot.send_message(chat_id=user_id, text=curr_quest['question'])
        curr_quest['message_id'] = msg.message_id

    elif curr_quest['type'] == 'info':
        completing_forms_dispatcher_remove_session(user_id=user_id)
        print('theend')
        print(completing_forms_dispatcher)


def lambda_checker_poll(pollAnswer: types.PollAnswer):
    """Проверяет принадлежит ли опрос выбранной форме"""
    if pollAnswer.user.id in completing_forms_dispatcher.keys():
        curr_question_num = 0
        selected_form = completing_forms_dispatcher_get_form_copy(pollAnswer.user.id)
        print(selected_form)
        print(selected_form[curr_question_num])

        if selected_form[curr_question_num]['message_id'] == pollAnswer['poll_id']:
            selected_form.remove(
                {'question': selected_form[curr_question_num]['question'], 'options': selected_form[curr_question_num]['options'], 'message_id': selected_form[curr_question_num]['message_id'], 'type': 'poll'})

            return True
        # print('folss')
        return False


def lambda_checker_msg(message: types.Message):
    """Проверяет является ли сообщение ответом на вопрос из формы"""

    if message.chat.id in completing_forms_dispatcher.keys():
        curr_question_num = 0
        selected_form = completing_forms_dispatcher_get_form_copy(message.chat.id)

        if selected_form[curr_question_num]['message_id'] + 1 == message.message_id:
            selected_form.remove(
                {'question': selected_form[curr_question_num]['question'], 'message_id': selected_form[curr_question_num]['message_id'], 'type': 'msg'})
            # print('eh')
            # print(message.text)
            return True
        # print('folss')
        return False


# handler activates when vote/send answer
async def poll_handler(pollAnswer: types.PollAnswer):
    """Активируется, когда приходит ответ на опрос/ опрос закрывается"""

    print(pollAnswer)
    if completing_forms_dispatcher:
        # print('go ahead pol')
        await go_cycle(message=pollAnswer, type='launch_from_poll_handler')
    # print(poll['id'])


async def msg_handlr(message: types.Message):
    """Активируется, когда приходит сообщение"""

    print(message)
    if completing_forms_dispatcher:
        # print('go ahead msg')
        await go_cycle(message=message, type='launch_from_message_handler')


def register_handlers_status(dp: Dispatcher):
    dp.register_message_handler(
        display_user_status, commands="status", state="*")
    dp.register_message_handler(
        complete_form, lambda message: message.text.startswith('/complete'))
    dp.register_poll_answer_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
    dp.register_message_handler(
        msg_handlr, lambda message: lambda_checker_msg(message))