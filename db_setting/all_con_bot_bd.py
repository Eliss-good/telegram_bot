from db_setting.poll_db.poll_connect_db import add_survay, add_answer_for_survay
from db_setting.register_db.all_register import reg_us
from db_setting.setter_db.all_setter_db import set_id_users, set_any_data, set_status_us, set_form, set_start_form_users, set_form_us, \
     set_form_name_for_form_id, set_from_id_for_tg_id
from db_setting.remove_db.all_delete import del_us
from db_setting.update_db.all_update import update_data_user, update_sub_news 
import db_setting.back_function_db as bf


###########################  БЛОК ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ################


####### Добавление препода
def add_prepod(fio: str, tg_id: int, role: str):
    reg_us(fio, tg_id, role)


####### Добавление студента
def add_st(fio: str, tg_id: int, role: str, group: str):
    reg_us(fio, tg_id, role, group_stud=group)


####### Выводит списком любые элементы
def list_all_data(command: str):
    return set_any_data(command)


####### Проверка на то зарегестрирован ли пользователь
def check_valid_us(tg_id: int):
   return set_status_us(tg_id)


####### Возвращает роль пользователя
def find_role_us(tg_id: int):
    return bf.find_role_us(tg_id)


####### Возвращает группу студента
def find_group_us(tg_id: int):
    return bf.find_group_us(tg_id)


####### Возвращает ФИО пользователя
def find_fio_us(tg_id: int):
    return bf.find_fio_us(tg_id)


####### Возврат id пользователей прикреплённых к группам
def find_us_for_survay(groups: list):
    return set_id_users(groups)


#####role: prepod / student; command: group / name
def update_user(role: str, command: str, new_data, id_us_tg: int):
    update_data_user(role ,command, new_data, id_us_tg)


##### механизм для редактирования подписки на рассылку #####
def update_news(id_us_tg: int, status: bool):
    update_sub_news(id_us_tg, status)


####### Удаление пользователя
def delete_user(tg_id: int):
    del_us(tg_id)


###################### БЛОК ДЛЯ РАБОТЫ С ФОРМАМИ ###################


####### Создание новой формы
def create_new_form(data_survay: list):
    add_survay(data_survay)


####### Добавление нового результата опроса
def add_new_answer(new_answer: dict):
    add_answer_for_survay(new_answer)


####### Кол-во созданных форм
def get_max_survay():
    return bf.max_code_survay()


##### Количество отправленных форм #####
def get_count_send_survay():
    return bf.find_count_send_form()


def get_start_survay(form_id: int, groups: list):
    """Возвращенеи формы для запуска опроса"""
    return set_start_form_users(form_id, groups)


##### Возвращение заготовленных форм из БД #####
def get_data_form(command: str, form_id = None):
    """command принимает значения ('all'/'any'/'one')"""
    return set_form(command, form_id)


def get_form_user(tg_id: int):
    """Отправляет все формы созданные поользователем"""
    return set_form_us(tg_id)


def get_name_form(form_id: int):
    """Отправляет имя формы по form_id"""
    return set_form_name_for_form_id(form_id)


def get_ids_create_form(tg_id: int):
    """Отправляет все id форм созданных по этому tg_id"""
    return set_from_id_for_tg_id(tg_id)



