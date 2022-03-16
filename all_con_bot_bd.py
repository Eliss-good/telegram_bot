import sys

sys.path.append('/home/eliss/ptoject/telegram_bot/db_setting')
import us_connect_db as us_db
import poll_connect_db as poll_db



###########################  БЛОК ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ################

####### Добавление препода
def add_prepod(fio, rg_id , role):
    us_db.reg_us(fio, id ,role)


####### Добавление студента
def add_st(fio, tg_id, role, group):
    us_db.reg_us(fio, tg_id, role, group_stud = group)


####### Выводит списком все группы
def list_all_group():
    return us_db.pars_data_spisok('group')


####### Проверка на то зарегестрирован ли пользователь
def check_valid_us(tg_id):
   return us_db.ck_data_db(tg_id)


####### Возвращает роль пользователя
def find_role_us(tg_id):
    return us_db.bf.db.select_db_where('global_tb', ['gl_role'], ['gl_teleg_id'], [str(tg_id)], 'where')[0][0]


####### Проверка на то зарегестрирован ли пользователь
def find_us_for_survay(groups):
    users_id_list = us_db.find_teleg_group(groups)


#####role: prepod / student; command: group / name
def update_data user(role ,command, new_data, id_us_tg):
    us_db.update_data_user(role ,command, new_data, id_us_tg)


##### механизм для редактирования подписки на рассылку #####
def update_sub_news(id_us_tg, status):
    us_db.update_sub_news(id_us_tg, status)


####### Удаление пользователя
def delete_user(tg_id):
    us_db.del_us(tg_id)



###########################  БЛОК ДЛЯ РАБОТЫ С ФОРМАМИ ###################


####### Создание новой формы
def create_new_form(from_id, to_group, data_survay):
    poll_db.add_survay(from_id, to_group, data_survay)


####### Добавление нового результата опроса
def add_new_answer(new_answer):
    poll_db.add_answer_for_survay(new_answer)