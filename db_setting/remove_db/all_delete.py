from .. import back_function_db as bf

def __del_prepod(tg_id):
    """Удаление преподавателя"""
    name_prepod = bf.find_fio_us(tg_id)
    id_prepod = bf.find_id_prepod(name_prepod)

    for item_pr in id_prepod:
        bf.db.delete_db('connect_tb', ['prepod_id'], [str(item_pr[0])])
    
    bf.db.delete_db('prepod_tb', ['gl_id'], [bf.find_id_global(str(tg_id))])
    bf.db.delete_db('global_tb', ['gl_teleg_id'], [bf.correct_str(str(tg_id))])


def __del_student(tg_id):
    """Удаление студента"""
    bf.db.delete_db('student_tb', ['gl_id'], [bf.find_id_global(tg_id)])
    bf.db.delete_db('global_tb', ['gl_teleg_id'], [bf.correct_str(str(tg_id))])

def del_us(tg_id):
    """Блок для определения роли под удаление"""
    find_tg_role = bf.find_role_us(tg_id)
    
    if find_tg_role != (0,):
        if find_tg_role == 'prepod':
            __del_prepod(tg_id)
        elif find_tg_role == 'student':
            __del_student(tg_id)
    else:
        print(tg_id, ' ещё не существует, зарегистрируйтесь')
