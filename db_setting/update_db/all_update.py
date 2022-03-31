import db_setting.back_function_db as bf


def update_sub_news(id_us_tg, status):
    """механизм для редактирования подписки на рассылку"""
    bf.db.update_db('global_tb', ['sub_newslet'], [str(status)], ['gl_teleg_id'], [bf.correct_str(str(id_us_tg))])


def update_aprove(tg_id : int):
    """Обновление информации о подтверждение препода"""
    if bf.find_role_us(tg_id) == 'prepod':
        global_id_pr = bf.find_id_global(tg_id)
        bf.db.update_db('prepod_tb', ['prepod_approved'], ['True'], ['gl_id'], [tg_id])
        

#####role: prepod / student; command: group / name 
def update_data_user(role ,command, new_data, id_us_tg):
    """Обновление данных о пользователей"""
    id_global = bf.find_id_global(id_us_tg)

    if command == 'name':
        bf.db.update_db(role + '_tb', [role + '_' + command], [bf.correct_str(new_data)], ['gl_id'], [str(id_global)])

    elif command == 'group' and role == 'student':
        id_group = bf.find_id_group(new_data)
        bf.db.update_db(role + '_tb', [command + '_id'], [id_group], ['gl_id'], [str(id_global)])