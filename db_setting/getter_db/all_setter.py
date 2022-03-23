import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as poll_db

"""Геттер для данных пользователя"""
def get_id_users(list_name_group):
    """Возвоащается списком  все ID телеги по указанным группам"""
    group_us = []

    for name_group in list_name_group:
        name_group[0] = name_group[0].upper()

        data = bf.db.select_db_where('student_tb', ['gl_id'], ['group_id'], [bf.find_id_group(name_group[0])], 'where')
        for i in data:
            group_us.append(bf.find_id_global(i))

    return group_us


def get_any_data(command):
    """Списком возвращается любая информация из таблиц"""
    all_data = bf.db.select_db(command + '_tb', [command + '_name'])
    all_data_norm = []
    for item in all_data:
        all_data_norm.append(item[0])

    return all_data_norm 


def get_status_us(tg_id):
    """Проверка на то зареган ли пользователь"""
    id = bf.find_id_global(tg_id)

    if int(id) == 0:
        return False
    else:
        return True


"""Геттер для опросов"""
def get_form(command, form_id = None):
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

    