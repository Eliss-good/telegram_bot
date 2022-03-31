
import db_setting.back_function_db as bf
import db_setting.poll_db.poll_connect_db as pl


def update_sub_news(id_us_tg, status):
    """механизм для редактирования подписки на рассылку"""
    bf.db.update_db('global_tb', ['sub_newslet'], [str(status)], ['gl_teleg_id'], [bf.correct_str(str(id_us_tg))])


def update_aprove_prepod(tg_id : int):
    """Обновление информации о подтверждение препода"""
    if bf.find_role_us(tg_id) == 'prepod':
        global_id_pr = bf.find_id_global(tg_id)
        bf.db.update_db('prepod_tb', ['prepod_approved'], ['True'], ['gl_id'], [global_id_pr])


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
def update_data_user(role: str, command: str, new_data, id_us_tg : int):
    """Обновление данных о пользователей"""
    id_global = bf.find_id_global(id_us_tg)

    if command == 'name':
        bf.db.update_db(role + '_tb', [role + '_' + command], [bf.correct_str(new_data)], ['gl_id'], [str(id_global)])

    elif command == 'group' and role == 'student':
        id_group = bf.find_id_group(new_data)
        bf.db.update_db(role + '_tb', [command + '_id'], [id_group], ['gl_id'], [str(id_global)])