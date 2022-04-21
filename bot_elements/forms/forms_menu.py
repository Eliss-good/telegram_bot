""" Меню для системы опросов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from bot_elements.getter.all_getters import get_all_groups, get_choosing_groups_dispatcher_user, get_chosen_groups_data, get_group_users_ids, get_temp_form_index_data, mem_for_created_forms_get_creator_id, registerData_get_fio, unique_sent_form_id_get, registerData_check_is_registered

from bot_elements.setter.all_setters import choosing_groups_dispatcher_add_user, chosen_groups_data_add_group, send_forms_mem_add_sent_form, temp_form_index_data_add_index, unique_sent_form_id_plus_one

from bot_elements.remover.all_removers import choosing_groups_dispatcher_remove_poll, choosing_groups_dispatcher_remove_user, chosen_groups_data_remove_user, temp_form_index_data_remove_index

from bot_elements.forms.form_display import display_current_mem_status

from bots import prepod_bot
# check forms mass and select user_ids + send forms in forms.py


async def choose_group(message: types.Message, state: FSMContext):
    """ Спрашивает юзера"""
    form_index = message.text[6:]

    temp_form_index_data_add_index(user_id=message.chat.id, form_index=form_index)

    if message.chat.id == mem_for_created_forms_get_creator_id(form_id=int(form_index)):
        
        all_groups = get_all_groups()
        send_poll_counter = 0


        while len(all_groups) > 10:
            temp_groups_list = all_groups[:9]
            temp_groups_list.append('Ни одна из вышеперечисленных')

            all_groups = all_groups[9:]
            # print('\n ala ', all_groups)
            msg = await prepod_bot.send_poll(chat_id=message.chat.id, question='Выберите получателей', options=temp_groups_list.copy(), is_anonymous=False, allows_multiple_answers=True)

            choosing_groups_dispatcher_add_user(user_id=message.chat.id, poll_id=msg.poll.id, options = temp_groups_list.copy(), poll_number=send_poll_counter)
            send_poll_counter += 1
            temp_groups_list.clear()


        if all_groups and len(all_groups) > 0:
            msg = await prepod_bot.send_poll(chat_id=message.chat.id, question='Выберите получателей', options=all_groups.copy(), is_anonymous=False, allows_multiple_answers=True)

            choosing_groups_dispatcher_add_user(user_id=message.chat.id, poll_id=msg.poll.id, options=all_groups.copy(), poll_number=send_poll_counter)

        send_poll_counter = 0
        
        # await sender.waiting_for_groups.set()

    else:
        message.answer('Вы не являетесь создателем формы')


def lambda_checker_poll(pollAnswer: types.PollAnswer):
    """ Проверяет опрос"""
    
    disp = get_choosing_groups_dispatcher_user(pollAnswer.user.id)

    if disp:
        for groups_poll_number in disp:
            if disp[groups_poll_number]['poll_id'] == pollAnswer['poll_id']:
    
                return True

    return False


async def poll_handler(pollAnswer: types.PollAnswer):
    """Активируется, когда приходит ответ на опрос/ опрос закрывается"""

    disp = get_choosing_groups_dispatcher_user(pollAnswer.user.id)
    
    if disp:
        for groups_poll_number in disp:
            if disp[groups_poll_number]['poll_id'] == pollAnswer['poll_id']:

                print('\n\n ---', disp)
                print('\n\n the fuck', pollAnswer.option_ids)
                print(' \n lol', disp[groups_poll_number]['options'])

                chosen_groups_data_add_group(user_id=pollAnswer.user.id, options_ids=pollAnswer.option_ids, groups=disp[groups_poll_number]['options'])
               
                choosing_groups_dispatcher_remove_poll(user_id=pollAnswer.user.id, poll_id=pollAnswer['poll_id'])
                break
    
    
    disp = get_choosing_groups_dispatcher_user(pollAnswer.user.id)
    
    if not disp:
        choosing_groups_dispatcher_remove_user(user_id=pollAnswer.user.id) 
        groupz = get_chosen_groups_data(user_id=pollAnswer.user.id)
        
        if 'Ни одна из вышеперечисленных' in groupz:
            groupz = [x for x in groupz if x != 'Ни одна из вышеперечисленных']

        send_to_users = get_group_users_ids(groups=groupz)


        form_creator_user_id = mem_for_created_forms_get_creator_id(int(get_temp_form_index_data(pollAnswer.user.id)))
        # получить id юзеров по группам
        send_forms_mem_add_sent_form(form_id=int(get_temp_form_index_data(pollAnswer.user.id)), sent_form_id=unique_sent_form_id_get(), form_creator_user_id=form_creator_user_id, send_to_users_ids=send_to_users, groups=groupz)
        
        temp_form_index_data_remove_index(pollAnswer.user.id)
        chosen_groups_data_remove_user(pollAnswer.user.id)
        unique_sent_form_id_plus_one()
        
        await prepod_bot.send_message(text='Отправлено группам ' + ''.join(str(groupz)), reply_markup=types.ReplyKeyboardRemove(), chat_id=pollAnswer.user.id)


def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
    dp.register_message_handler(choose_group, lambda message: message.text.startswith('/send'))
    dp.register_poll_answer_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
