from create_file.create_csv.create_groups_list import create_file_group
from db_setting.getter_db.all_getter_db import update_sending_status
import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as poll_db

"""Cеттер для данных пользователя"""
def set_id_users(list_name_group : list, form_id: int = None):
    """Возвоащается списком  все ID телеги по указанным группам"""
    group_us = []
    
    if list_name_group :
        for name_group in list_name_group:
            #name_group[0] = name_group[0].upper()

            data = bf.db.select_db_where('student_tb', ['gl_id'], ['group_id'], [bf.find_id_group(name_group)], 'where')
            for i in data:
                group_us.append(int(bf.find_tg_id(i[0])))

        if form_id != None:
            update_sending_status(form_id)
            
            poll_db.all_users_send_form(group_us,form_id)
            poll_db.all_groups_form(list_name_group, form_id)


        return group_us


def set_any_data(command):
    """Списком возвращается любая информация из таблиц"""
    all_data = bf.db.select_db(command + '_tb', [command + '_name'])
    all_data_norm = []
    for item in all_data:
        all_data_norm.append(item[0])

    return all_data_norm 


def set_status_us(tg_id):
    """Проверка на то зареган ли пользователь"""
    id = bf.find_id_global(tg_id)

    if int(id) == 0:
        return False
    else:
        return True


"""Cеттер для опросов"""


def set_form(command, form_id = None):
    """Отправление уже готовых форм боту"""
    data = poll_db.read_answer_to_file()

    if command == 'all' and form_id == None:
        return data

    elif  command == 'one' and type(form_id) == int:
        return bf.find_one_form(data, form_id)

    elif command == 'any' and type(form_id) == list:
        all_forms = []
        for item in form_id:
            all_forms.append(bf.find_one_form(data, item))
        return all_forms


def set_start_form_users(form_id, groups):
    """Отправка телеграм боту новой формы"""
    bf.db.update_db('survay_tb', ['sending_status'], ['True'], ['form_id'], [bf.correct_str(str(form_id))])

    """Добавление в инфо о форме список групп, которым приходит эта форма"""
    groups = ["М3О-221Б-20", "М3О-212Б-20", "М3О-214Б-20"]
    poll_db.add_to_sub_form(form_id, groups)
    return set_form('one', form_id)


def set_form_us(tg_id: int):
    """Все формы созданные по tg_id"""

    if bf.find_role_us(tg_id) != 'prepod':
        """Проверка на то преподаватель ли пользователь"""
        return None

    tg_id = bf.correct_str(str(tg_id))
    id_forms = bf.db.select_db_where('survay_tb', ['form_id'], ['from_id'], [tg_id], 'where')

    user_forms = []
    for item_id in id_forms:
        try:
            info_form = set_form('one', form_id=item_id[0])

            if info_form != None:
                user_forms.append(info_form)
        except IndexError:
            print('INDEX ERROR fun', set_form_us.__name__)

    return user_forms


def set_from_id_for_tg_id(tg_id : int):
    """Возвращеник списком id всех форм созданных по tg_id"""
    list_forms = bf.db.select_db_where('survay_tb', ['form_id'], ['from_id'], [tg_id], 'where')
    return bf.correct_list(list_forms)


def set_form_name_for_form_id(form_id : int):
    """Возвращает имя формы по form_id"""
    return bf.find_name_form(form_id)


def set_all_groups_for_prepod(tg_id : int):
    """Вывод всех групп прикреплённых преподавателю"""
    id_prepod = bf.find_id_prepod_for_tg(tg_id)
    id_groups = bf.db.select_db_where('connect_tb', ['group_id'], ['prepod_id'], [id_prepod], 'where')

    id_groups = bf.correct_list(id_groups)
    name_groups = []

    for one in id_groups:
        name_groups.append(bf.find_name_group(one))

    return name_groups


def set_all_groups_from_prepod(tg_id: int):
    """Вывод всех пользователей прикреплённых преподавателю"""
    groups_prepod = set_all_groups_for_prepod(tg_id)
    all_users = {}

    for one_gr in groups_prepod:
        all_users[one_gr] = set_id_users([one_gr])

    return all_users


def set_tg_user_for_from(form_id: int):
    """Возвращает id пользователя, который создал форму"""
    return int(bf.db.select_db_where('survay_tb', ['from_id'], ['form_id'], [str(form_id)], 'where')[0][0])


def set_status_authenticity(tg_id: int):
    return bf.authenticity_check(tg_id)


def set_send_form_user(sent_form_id: int):
    """Возвращенеи всех id пользователей которым отослана форма"""
    id_survey = bf.find_id_survay(sent_form_id)

    if id_survey:
        list_groups = poll_db.find_groups_is_form(sent_form_id)
        list_users = set_id_users(list_groups)
        return list_users
    else:
        return []


def get_max_survay():
    """Кол-во созданных форм"""
    return bf.max_code_survay()


def get_count_send_survay():
    """Кол-во отправленных форм"""
    return bf.find_count_send_form()


def find_role_us(tg_id: int):
    """Возвращает роль пользователя"""
    return bf.find_role_us(tg_id)


def find_group_us(tg_id: int):
    """Возвращает группу студента"""
    return bf.find_group_us(tg_id)


def find_fio_us(tg_id: int):
    """Возвращает ФИО пользователя"""
    return bf.find_fio_us(tg_id)


def find_all_us_is_group(groups: list):
    """Возвращает фамилии людей по группе"""
    fio_users = {}
    
    for one_group in groups:
        fio_users[one_group] = []
        tg_users = set_id_users([one_group])

        for one_us in tg_users:
            fio_users[one_group].append(find_fio_us(int(one_us)))

    dir = create_file_group(fio_users)
    return dir


def formatted_data_user():
    """Форматирование данных для бота"""
    user_name = bf.db.select_db_where('global_tb', ['gl_role'], ['gl_approved'], ['False'], 'where')
    user_gl_id = bf.db.select_db_where('global_tb', ['gl_teleg_id'], ['gl_approved'], ['False'], 'where')

    formate_all_data = {}
    for i in range (0,len(user_name)):
        name_us = bf.find_fio_us(user_gl_id[i][0])

        info_for_us = {'chosen_fio' : name_us, 'chosen_role' : 'prepod', 'confirmed' : False } 
        formate_all_data[user_gl_id[i][0]] = info_for_us

    return formate_all_data
