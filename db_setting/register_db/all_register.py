import db_setting.back_function_db as bf

def __student_start(name_user: str, id_us_tg: int, name_group: str):
    bf.add_group(name_group, True)
    bf.add_student(name_user, id_us_tg, name_group)
    #bf.start_gr(name_group)


def __prepod_start(name_user: str, id_us_tg: int):
    bf.add_prepod(name_user, tg_id  = id_us_tg)
    #bf.start_pr(input("введите ссылку на препода: "))


def __admin_start(name_user: str, tg_id: int):
    bf.add_admin('xyi', tg_id)


def reg_us(name_user, id_us_tg, role, group_stud = None):
    print(group_stud, role)

    if bf.add_us(id_us_tg, role):
        if role == 'student' and group_stud != None:
            __student_start(name_user, id_us_tg, group_stud)
        elif role == 'prepod' and group_stud == None:
            __prepod_start(name_user, id_us_tg)
        elif role == 'admin' and group_stud == None:
            __admin_start(name_user, id_us_tg)
    
    else:
        #update_us(id_us_tg)
        print(id_us_tg ,' ты уже зареган')


