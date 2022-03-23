from db_setting.poll_db.poll_connect_db import add_survay, add_answer_for_survay
from db_setting.register_db.all_register import reg_us
from db_setting.getter_db.all_setter import get_id_users,get_any_data,get_status_us, get_form
from db_setting.remove_db.all_delete import del_us
from db_setting.update_db.all_update import update_data_user, update_sub_news 
import db_setting.back_function_db as bf


###########################  БЛОК ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ################


####### Добавление препода
def add_prepod(fio, rg_id , role):
    reg_us(fio, rg_id ,role)


####### Добавление студента
def add_st(fio, tg_id, role, group):
    reg_us(fio, tg_id, role, group_stud = group)


####### Выводит списком любые элементы
def list_all_group(command):
    return  get_any_data(command)


####### Проверка на то зарегестрирован ли пользователь
def check_valid_us(tg_id):
   return  get_status_us(tg_id)


####### Возвращает роль пользователя
def find_role_us(tg_id):
    return  bf.find_role_us(tg_id)


####### Возвращает группу студента
def find_group_us(tg_id):
    return  bf.find_group_us(tg_id)


####### Возвращает ФИО пользователя
def find_fio_us(tg_id):
    return  bf.find_fio_us(tg_id)


####### Возврат id пользователей прикреплённых к группам
def find_us_for_survay(groups):
    return  get_id_users(groups)


#####role: prepod / student; command: group / name
def update_data_user(role ,command, new_data, id_us_tg):
    update_data_user(role ,command, new_data, id_us_tg)


##### механизм для редактирования подписки на рассылку #####
def update_sub_news(id_us_tg, status):
    update_sub_news(id_us_tg, status)


####### Удаление пользователя
def delete_user(tg_id):
    del_us(tg_id)


###################### БЛОК ДЛЯ РАБОТЫ С ФОРМАМИ ###################


####### Создание новой формы
def create_new_form(from_id, to_group, data_survay):
    add_survay(from_id, to_group, data_survay)


####### Добавление нового результата опроса
def add_new_answer(new_answer):
    add_answer_for_survay(new_answer)


##### Возвращение заготовленных форм из БД #####
def get_data_form(command, form_id = None):
    """command принимает значения ('all'/'any'/'one')"""
    return get_form(command, form_id)
