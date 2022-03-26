import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as poll_db

"""Cеттер для данных пользователя"""
def set_id_users(list_name_group):
    """Возвоащается списком  все ID телеги по указанным группам"""
    group_us = []

    for name_group in list_name_group:
        name_group[0] = name_group[0].upper()

        data = bf.db.select_db_where('student_tb', ['gl_id'], ['group_id'], [bf.find_id_group(name_group[0])], 'where')
        for i in data:
            group_us.append(int(bf.find_tg_id(i[0])))

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


def set_form_us(tg_id):
    """Все формы созданные по tg_id"""

    if bf.find_role_us(tg_id) == 'student':
        """Проверка на то преподаватель ли пользователь"""
        return None

    tg_id = bf.correct_str(str(tg_id))
    id_forms = bf.db.select_db_where('survay_tb', ['form_id'], ['from_id'], [tg_id], 'where')

    user_forms = []
    for item_id in id_forms:
        try:
            user_forms.append(set_form('one', form_id=item_id[0]))
        except IndexError:
            print('INDEX ERROR fun', set_form_us.__name__)

    return user_forms
