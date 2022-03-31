from bots import admin_bot
from aiogram import types, Dispatcher
from bot_elements.getter.all_getters import temp_mem_for_form_creator_get, mem_for_created_forms_get, completing_forms_dispatcher_get, send_forms_mem_get, temp_form_recipient_data_get_recip_data, registerData_get_fio, mem_for_created_forms_get_form_name


async def display_temp_mem_for_form_creator(message: types.Message):

    """ 
    Формат:
    {506629389: [{'question': 'Тел', 'message_id': 0, 'type': 'msg'}, {'question': 'Одна', 'options': ['Ладно', ' роз'], 'message_id': 0, 'type': 'poll'}]}
    (recip_data)  {'form_name': 'Такое', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}
    """

    temp_mem_data = temp_mem_for_form_creator_get()

    if temp_mem_data:

        full_message = ""
        for user_id in temp_mem_data:
            recip_info = temp_form_recipient_data_get_recip_data(user_id)
            if recip_info:
                full_message += 'NAME: ' + \
                    str(recip_info['form_name']) + ' BY: ' + \
                    str(registerData_get_fio(user_id)) + '\n'
            if not recip_info:
                full_message += 'NAME: ' + 'имя не выбрано' + \
                    ' BY: ' + str(registerData_get_fio(user_id)) + '\n'

            current_form = temp_mem_data[user_id]

            for element in current_form:
                if element['type'] == 'msg':
                    full_message += 'Question: ' + \
                        str(element['question']) + '\n'

                elif element['type'] == 'poll':
                    full_message += 'Poll name: ' + \
                        str(element['question']) + ' Options: ' + \
                        str(element['options']) + '\n'
        full_message += '\n' + '-----' + '\n'
        await admin_bot.send_message(text=full_message, chat_id=message.chat.id)
    else:
        await admin_bot.send_message(text='В настоящий момент никто не создает формы', chat_id=message.chat.id)


async def display_mem_for_created_forms(message: types.Message):
    """
    Пример mem_for_created_forms:
    {0: [{'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}], 1: [{'question': 'Зе криэтир', 'options': ['Один', ' два'], 'message_id': 0, 'type': 'poll'}, {'form_name': 'Тайлер', 'type': 'info', 'form_id': 1, 'creator_id': 506629389}]}
    """

    mem_data = mem_for_created_forms_get()
    if mem_data:
        full_text = ''
        for message_id in mem_data:
            selected_form = mem_data[message_id]
            full_text += 'NAME: ' + str(selected_form[-1]['form_name']) + ' BY: ' + str(
                registerData_get_fio(selected_form[-1]['creator_id'])) + '\n'

            for element in selected_form:
                if element['type'] == 'msg':
                    full_text += 'question: ' + element['question'] + '\n'

                elif element['type'] == 'poll':
                    full_text += 'question: ' + \
                        element['question'] + ' options: ' + \
                        str(element['options']) + '\n'
        full_text += '\n' + '------' + '\n'
        await admin_bot.send_message(chat_id=message.chat.id, text=full_text)

    else:
        await admin_bot.send_message(chat_id=message.chat.id, text='Нет созданных форм')


async def display_send_forms_mem(message: types.Message):
    """ 
    Формат send_forms_mem
    {'sent_form_id': {'form_id': *form_id*, 'info': {'form_creator_user_id': id,'send_to_users_ids': [ids], 'send_to_groups': [groups], 'got_answers_from': [ids]}, ...} 

    """
    send_forms_mem = send_forms_mem_get()
    if send_forms_mem:
        full_text = ''
        for form_id in send_forms_mem:
            select_form = send_forms_mem[form_id]
            full_text += 'NAME: ' + str(mem_for_created_forms_get_form_name(form_id=form_id)) + ' SENT TO: ' + str(
                select_form['info']['send_to_groups']) + ' got_answers_from: ' + str(select_form['info']['got_answers_from']) + '\n'

        await admin_bot.send_message(text=full_text, chat_id=message.chat.id)

    else:
        await admin_bot.send_message(
            text='Нет отправленных форм', chat_id=message.chat.id)


async def display_completing_forms_dispatcher(message: types.Message):
    """
    Формат:
    {'user_id': {''unique_form_id'': id, 'unique_sent_form_id': id, 'current_question': num, 'form_copy': [form_data]}, ...}
    """
    """
    Пример form_data:
    {'question': 'Сос', 'options': ['Лан', ' все'], 'message_id': 0, 'type': 'poll'}, {'question': 'Месяц', 'message_id': 0, 'type': 'msg'}, {'form_name': 'Формо', 'type': 'info', 'form_id': 0, 'creator_id': 506629389}], 1: [{'question': 'Зе криэтир', 'options': ['Один', ' два'], 'message_id': 0, 'type': 'poll'}, {'form_name': 'Тайлер', 'type': 'info', 'form_id': 1, 'creator_id': 506629389}
    """

    completing_forms_mem = completing_forms_dispatcher_get()
    if completing_forms_mem:
        full_text = ''
        for user_id in completing_forms_mem:
            selected_form = completing_forms_mem[user_id]
            full_text += 'COMPLETING BY: ' + user_id + ' FORM NAME: ' + \
                selected_form['form_copy'][-1]['form_name'] + \
                'CURR QUESTION: ' + selected_form['current_question'] + '\n'

        await admin_bot.send_message(text=full_text, chat_id=message.chat.id)

    else:
        await admin_bot.send_message(
            text='Сейчас никто не проходит опросы', chat_id=message.chat.id)


def register_handlers_forms_check_storages(dp: Dispatcher):
    dp.register_message_handler(
        display_temp_mem_for_form_creator, commands='check_current_creating_forms')
    dp.register_message_handler(
        display_mem_for_created_forms, commands='check_created_forms')
    dp.register_message_handler(
        display_send_forms_mem, commands='check_sent_forms')
    dp.register_message_handler(
        display_send_forms_mem, commands='check_completing_forms')

