from .db_connect import DataConnect

db = DataConnect()


def correct_str(t_item):
    """служебная функция"""
    t_item = "'" + t_item +"'" 
    return t_item 

def correct_list(old_list):
    new_list = []
    for one_item in old_list:
        new_list.append(one_item[0])
    return new_list



        ################## insurt_modul ##################
def add_us(tg_id, role):
    """Добавление нового пользователя"""
    tg_id = correct_str(str(tg_id))
    role = correct_str(str(role))

    tg_id_ck = db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [tg_id],'check')
    if tg_id_ck:
        db.insert_db('global_tb', ['gl_teleg_id', 'gl_role'], [tg_id, role])
        return True
    else:
        print(tg_id, ' уже существует')
        return False


def add_lesson(name_lesson):
    """Добавление нового предмета"""
    name_lesson = correct_str(str(name_lesson))

    lesson_ck = db.select_db_where('lesson_tb', ['id'], ['lesson_name'] ,[name_lesson],'check')
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [name_lesson])
    else:
        print(name_lesson, ' уже существует')


def add_prepod(name_prepod, tg_id = 1):
    """Добаление нового преподавателя,
     в tg_id ничего не подаётся в случае если идёт заполение с парсеров """
    con_data =[correct_str(name_prepod), find_id_global(tg_id)]
    prepod_ck = db.select_db_where('prepod_tb', ['id'], ['prepod_name', 'gl_id'], con_data, 'check')
    prepod_ck_auto_us = db.select_db_where('prepod_tb', ['id'], ['prepod_name', 'gl_id'], [correct_str(name_prepod), find_id_global(1)], 'check')

    if prepod_ck and tg_id != 1 and not prepod_ck_auto_us:
        db.update_db('prepod_tb', ['gl_id'], [find_id_global(tg_id)], ['prepod_name'], [correct_str(name_prepod)])
    elif prepod_ck and tg_id != 1 and prepod_ck_auto_us:
        db.insert_db('prepod_tb', ['prepod_name', 'gl_id'], con_data)


def add_group(name_group, status):
    """Добавление новой группы"""
    name_group = correct_str(str(name_group))
    status = correct_str(str(status))

    if db.select_db_where('group_tb', ['id'], ['group_name', 'group_approved']  ,[name_group, status], 'check'):
        db.insert_db('group_tb', ['group_name', 'group_approved'] , [name_group, status])
    else:
        print(name_group, ' уже существует')


def add_student(name_student, tg_id, name_group):
    """Добавление студента"""
    name_student = correct_str(str(name_student))
    con_data =[name_student, find_id_group(name_group)]

    if db.select_db_where('student_tb', ['id'], ['student_name', 'group_id' ]  ,con_data, 'check'):
        con_data.append(find_id_global(tg_id))
        db.insert_db('student_tb', ['student_name', 'group_id', 'gl_id'], con_data)
    else:
        print(name_student, name_group,' уже существует')


        ################## select_modul ##################
def find_id_group(name_group):
    """Возвращение предмета по группе"""
    name_group = correct_str(str(name_group))

    try:
        return str(db.select_db_where('group_tb', ['id'], ['group_name'], [name_group], 'where')[0][0])
    except IndexError:
        print('INDEX ERROR fun', find_id_group.__name__)


def find_id_lesson(name_lesson):
    """Возвращение ID предмета"""
    name_lesson = correct_str(str(name_lesson))

    try:
        return str(db.select_db_where('lesson_tb', ['id'], ['lesson_name'], [name_lesson], 'where')[0][0])
    except:
        print('INDEX ERROR fun', find_id_lesson.__name__)


def find_id_prepod(name_prepod):
    """Возвращение ID препода"""
    name_prepod = correct_str(str(name_prepod))

    try:
        return str(db.select_db_where('prepod_tb', ['id'], ['prepod_name'], [name_prepod], 'where')[0][0])
    except:
        print('INDEX ERROR fun', find_id_prepod.__name__)

def find_id_global(tg_id):
    """Возвращение ID пользователя из глобальной таблицы"""
    tg_id = correct_str(str(tg_id))

    data = db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [tg_id],'where')
    if data != []: 
        print(data)
        return str(data[0][0])
    else:
        return '0'


def find_id_group_student(tg_id):
    """Возвращение ID группы студента пользователя"""
    try:
        return db.select_db_where('student_tb', ['group_id'], ['gl_id'], [find_id_global(tg_id)], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_role_us.__name__)

def find_role_us(tg_id):
    """Возвращение роли пользователя"""
    tg_id = correct_str(str(tg_id))

    try:
        return db.select_db_where('global_tb', ['gl_role'], ['gl_teleg_id'], [tg_id], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_fio_us.__name__)

def find_fio_us(tg_id):
    """Возвращение фио пользователя"""
    role = find_role_us(tg_id)

    try:
        return db.select_db_where(role + '_tb', [role + '_name'], ['gl_id'], [find_id_global(tg_id)], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_fio_us.__name__)


def find_group_us(tg_id):
    """Возвращение группы пользователя"""
    try:
        return db.select_db_where('group_tb', ['group_name'], ['id'], [(find_id_group_student(tg_id))], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_group_us.__name__)


def find_tg_id(gl_id):
    try:
        return db.select_db_where('global_tb', ['gl_teleg_id'], ['id'], [gl_id], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_tg_id.__name__)


def connect_gr_th(name_group, t_item):
    """Добавление связи в таблицу connect (преподаватель; группа; предмет)"""
    con_data = [find_id_group(name_group), find_id_prepod(t_item['prepod']), find_id_lesson(t_item['lesson']), correct_str(t_item['role'])]
    
    name_group = correct_str(str(name_group))
    t_item['role'] = correct_str(str(t_item['role']))
    t_item['lesson'] = correct_str(str(t_item['lesson']))
    t_item['prepod'] = correct_str(str(t_item['prepod']))

    if db.select_db_where('connect_tb', ['id'], ['group_id','prepod_id', 'lesson_id', 'teach_role'], con_data, 'check'):
        db.insert_db('connect_tb', ['group_id','prepod_id', 'lesson_id', 'teach_role'], con_data)
    

"""Функционал для опросов"""


def add_questions(question_n):
    question_n = correct_str(question_n)
    ques_ck = db.select_db_where('question_tb', ['id'], ['question_name'], [question_n], 'check')

    if ques_ck:
        db.insert_db('question_tb', ['question_name'], [question_n])


def add_group_questions(question_n, group_id):
    ques_ck = db.select_db_where('groupquestion_tb', ['q_id'], ['q_id', 'gp_question_id' ],[str(find_id_question(question_n)), group_id], 'check')

    if ques_ck:
        db.insert_db('groupquestion_tb', ['q_id', 'gp_question_id' ],[str(find_id_question(question_n)), group_id])


def find_id_survay(form_id):
    """Возвращение id формы"""
    form_id = correct_str(str(form_id))

    try:
        return db.select_db_where('survay_tb', ['id'], ['form_id'], [form_id], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_id_survay.__name__)


def find_id_question(question_n):
    """Возврапщение id вопроса"""
    question_n = correct_str(question_n)
    try:
        return db.select_db_where('question_tb', ['id'], ['question_name'], [question_n], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_id_question.__name__)


def find_name_form(form_id : int):
    form_id = correct_str(str(form_id))

    try:
        return db.select_db_where('survay_tb', ['form_name'], ['form_id'], [form_id], 'where')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_name_form.__name__)



def find_one_form(data, form_id):
    """Поиск формы в json с ответами"""
    data = data.get(str(find_id_survay(form_id)))

    if data != None:
        try:
            return data['info_form']
        except KeyError:
            print('KEY ERROR fun', find_one_form.__name__)
    else:
        print('Erorrchik')


def max_index_group_question():
    """Поиск максимального ID группы вопросов"""
    try:
        max_el = db.select_db_where('groupquestion_tb', ['gp_question_id'], [], [] ,'max')[0][0]

        if max_el == None:
            return 0
        else:
            return max_el
    except IndexError:
        print('INDEX ERROR fun', max_index_group_question.__name__)


def max_code_survay():
    """Возвращение максимального кода формы"""
    try:
        return db.select_db_where('survay_tb', ['form_id'], [], [] ,'max')[0][0]
    except IndexError:
        print('INDEX ERROR fun', max_code_survay.__name__)


def find_count_send_form():
    try:
        return db.select_db_where('survay_tb', ['form_id'], ['sending_status'], ['True'] ,'count')[0][0]
    except IndexError:
        print('INDEX ERROR fun', find_count_send_form.__name__)

