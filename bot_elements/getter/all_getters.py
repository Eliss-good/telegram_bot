from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages  import temp_mem_for_form_creator
from bot_elements.storages.all_storages  import mem_for_created_forms
from bot_elements.storages.all_storages  import send_forms_mem 
# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher

from bot_elements.storages.all_storages import completing_forms_dispatcher # {'user_id': {''unique_form_id'': id, 'unique_sent_form_id': id, 'curr_page': num, 'form_copy': [form_data]}, ...}
from bot_elements.storages.all_storages import registerData # {*user_id*: {'user_role': *role*, 'user_group': *group*}}


def temp_form_recipient_data_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую служебные данные (temp_form_recipient_data)"""
    return temp_form_recipient_data[user_id]


def temp_mem_for_form_creator_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую данные создаваемой формы (temp_mem_for_form_creator)"""
    return temp_mem_for_form_creator[user_id]


def mem_for_created_forms_get_data(form_id: int):
    """ Возвращает ячейку памяти хранящую данные созданной формы (mem_for_created_forms)"""
    return mem_for_created_forms[form_id]


def mem_for_created_forms_get_form_name(form_id: int):
    """ Возвращает название созданной формы из mem_for_created_forms"""
    return mem_for_created_forms[form_id][-1]['form_name']


def mem_for_created_forms_get_creator_id(form_id: int):
    """ Возвращает айди создателя формы из mem_for_created_forms"""
    return mem_for_created_forms[form_id][-1]['creator_id']


def completing_forms_dispatcher_get_form_copy(user_id: int):
    """ Возвращает копию формы из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy']


def registerData_get_fio(user_id: int):
    """ Возвращает ФИО юзера из registerData"""
    return registerData[user_id]['chosen_fio']


def registerData_get_group(user_id: int):
    """ Возвращает группу юзера из registerData"""
    return registerData[user_id]['chosen_group']


def registerData_get_role(user_id: int):
    """ Возвращает роль юзера из registerData"""
    return registerData[user_id]['chosen_role']

