from .. import back_function_db as bf

def set_id_users(list_name_group):
    group_us = []

    for name_group in list_name_group:
        name_group[0] = name_group[0].upper()

        data = bf.db.select_db_where('student_tb', ['gl_id'], ['group_id'], [bf.find_id_group(name_group[0])], 'where')
        for i in data:
            group_us.append(bf.find_id_global(i))

    return group_us


def set_any_data(command):
    all_data = bf.db.select_db(command + '_tb', [command + '_name'])
    all_data_norm = []
    for item in all_data:
        all_data_norm.append(item[0])

    return all_data_norm 


def set_status_us(tg_id):
    id = bf.find_id_global(tg_id)

    if int(id) == 0:
        return False
    else:
        return True