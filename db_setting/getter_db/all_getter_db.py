import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as poll_db
from db_setting.register_db.all_register import reg_us
from db_setting.poll_db.poll_connect_db import add_survay, add_answer_for_survay
from db_setting.update_db.all_update import update_data_user, update_sub_news, update_aprove, update_name_form, update_status_form
from db_setting.remove_db.all_delete import del_us


def add_prepod(fio: str, tg_id: int, role: str):
    """Добавление нового преподавателя"""
    reg_us(fio, tg_id, role)


def add_stud(fio: str, tg_id: int, role: str, group: str):
    """Добавление новго студента"""
    reg_us(fio, tg_id, role, group_stud=group)


def add_admin(fio: str, tg_id: int, role: str):
    """Добавление администратора"""
    reg_us(fio, tg_id, role)


def update_user(tg_id: int, name: str, role: str, group=None):
    """Обновление данных пользователя"""
    update_data_user(tg_id, name, role, group=group)


def update_news(id_us_tg: int, status: bool):
    """механизм для редактирования подписки на рассылку"""
    update_sub_news(id_us_tg, status)


def delete_user(tg_id: int):
    """Удаление пользователя"""
    del_us(tg_id)


def create_new_form(data_survay: list):
    """Создаёт новую форму"""
    add_survay(data_survay)


def add_new_answer(new_answer: dict):
    """Добавления нового результата опроса"""
    add_answer_for_survay(new_answer)


def update_status(tg_id: int, new_status: bool):
    """Обновляет статус подленности препода"""
    update_aprove(tg_id, new_status)


def update_form_name(form_id : int, new_name : str):
    """Обновляет название формы"""
    update_name_form(form_id, new_name)


def update_sending_status(form_id: int):
    """Подтверждение о отправке формы"""
    update_status_form(form_id)

#delete_user(622867137)
