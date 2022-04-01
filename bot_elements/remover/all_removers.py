from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData
from bot_elements.storages.all_storages import edited_register_data
# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher


def temp_form_recipient_data_remove_element(user_id: int):
    """ Убирает 1 элемент из temp_form_recipient_data"""
    temp_form_recipient_data.pop(user_id, None)


def temp_mem_for_form_creator_remove_form(user_id: int):
    """ Убирает 1 форму из temp_mem_for_form_creator"""
    temp_mem_for_form_creator.pop(user_id, None)


def temp_mem_for_form_creator_remove_form_element(user_id: int, delete_id: int):
    """ Убирает 1 элемент формы по delete_id из temp_mem_for_form_creator"""
    temp_mem_for_form_creator[user_id].pop(delete_id, None)


def mem_for_created_forms_delete_question(form_id: int, question_id: int):
    """ (Для БД) Убирает 1 элемент формы по question_id из mem_for_created_forms"""
    """ form_id - айди формы, question_id - айди вопроса"""
    if form_id in mem_for_created_forms.keys():
        mem_for_created_forms[form_id].pop(question_id)


def mem_for_created_forms_delete_form(form_id: int):
    """ (Для БД) Убирает 1 форму из mem_for_created_forms"""
    """ form_id - айди формы"""
    mem_for_created_forms.pop(form_id, None)


def completing_forms_dispatcher_remove_session(user_id: int):
    """ Убирает 1 активную сессию  из completing_forms_dispatcher"""
    completing_forms_dispatcher.pop(user_id, None)
    

def registerData_remove_user(user_id: int):
    registerData.pop(user_id, None)
    

def edited_register_data_remove_user(user_id: int):
    edited_register_data.pop(user_id, None)
