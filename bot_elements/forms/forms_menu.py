""" Меню для системы опросов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_elements.getter.all_getters import get_all_groups, get_group_users_ids, mem_for_created_forms_get_creator_id, registerData_get_fio, unique_sent_form_id_get

from bot_elements.setter.all_setters import send_forms_mem_add_sent_form, unique_sent_form_id_plus_one

from bot_elements.storages.all_storages import registerData

from bot_elements.forms.form_display import display_current_mem_status
# check forms mass and select user_ids + send forms in forms.py


class sender(StatesGroup):
    """FSM чтобы получать список групп"""
    waiting_for_groups = State()


async def choose_group(message: types.Message, state: FSMContext):
    """ (sender FSM) Спрашивает юзера"""
    form_index = message.text[6:]

    if message.chat.id == mem_for_created_forms_get_creator_id(form_id=int(form_index)):
    
        await state.update_data(form_index=form_index)
        # await message.reply('Напишите через запятую группы-получатели')

        final_string = "\nСписок доступных групп:"
        if get_all_groups():
            for data in get_all_groups():
                final_string += '\n' + str(data)

        else:
            final_string += '\n нет доступных групп'

        await message.reply('Выберите получателей (Введите группы, разделяя их запятыми)' + final_string)
        await sender.waiting_for_groups.set()

    else:
        message.answer('Вы не являетесь создателем формы')


async def sending(message: types.Message, state: FSMContext): # sender.waiting_for_groups
    """ (sender FSM) получает список групп и отправляет в send_forms_mem"""
    
    groups = message.text.split(',')
    print('\n\n send_to_grps ', groups)
    send_to_users = get_group_users_ids(groups=groups)


    final_data = await state.get_data()
    form_creator_user_id = mem_for_created_forms_get_creator_id(int(final_data['form_index']))
    # получить id юзеров по группам
    send_forms_mem_add_sent_form(form_id=int(final_data['form_index']), sent_form_id=unique_sent_form_id_get(), form_creator_user_id=form_creator_user_id, send_to_users_ids=send_to_users)

    unique_sent_form_id_plus_one()

    await message.answer('Отправлено группам ' + ''.join(str(send_to_users)), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
    dp.register_message_handler(choose_group, lambda message: message.text.startswith('/send'))
    dp.register_message_handler(sending, state=sender.waiting_for_groups)
