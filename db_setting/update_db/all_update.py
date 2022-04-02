import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as pl


def update_sub_news(id_us_tg: int, status: bool):
    """механизм для редактирования подписки на рассылку"""
    bf.db.update_db('global_tb', ['sub_newslet'], [str(status)], ['gl_teleg_id'], [bf.correct_str(str(id_us_tg))])


def update_aprove(tg_id : int, status: bool):
    """Обновление информации о подтверждение препода"""
    bf.db.update_db('global_tb', ['gl_approved'], [str(status)], ['gl_teleg_id'], [bf.correct_str(str(tg_id))])


def update_name_form(form_id: int, new_name: str):
    """Замена названия формы"""
    bf.db.update_db('survay_tb', ['form_name'], [new_name], ['form_id'],[str(form_id)])
    id_survey = bf.find_id_survay(form_id)

    try:
        full_data = pl.read_answer_to_file()
        full_data[id_survey]['info_form'][-1]['form_name'] = new_name
        pl.write_answer_to_file(full_data)
    except KeyError:
        print("ERROR fun", update_name_form.__name__)
    
    
#####role: prepod / student; command: group / name 
def update_data_user(tg_id: int, name_us: str, role: str, group=None):
    """Обновление данных о пользователей"""
    id_global = bf.find_id_global(tg_id)

    if role == 'student':
        id_groups = bf.find_id_group(group)
        bf.db.update_db('student_tb', ['student_name', 'group_id'], [bf.correct_str(name_us), id_groups], ['gl_id'], [str(id_global)])
    elif role == 'prepod':
        bf.db.update_db('prepod_tb', ['prepod_name'], [bf.correct_str(name_us)], ['gl_id'], [str(id_global)])