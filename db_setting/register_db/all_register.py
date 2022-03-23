import db_setting.back_function_db as bf

def __student_start(name_user, id_us_tg,name_group):
    bf.add_group(name_group, True)
    bf.add_student(name_user, id_us_tg, name_group)
    #bf.start_gr(name_group)

def __prepod_start(name_user, id_us_tg):
    
    bf._correct_data_prepod(name_user, id_us_tg)
    bf.add_prepod(name_user, id_us_tg  = id_us_tg)
    #bf.start_pr(input("введите ссылку на препода: "))


def reg_us(name_user, id_us_tg, role, group_stud = None):
    print(group_stud, role)

    if bf.add_us(id_us_tg, role):
        if role == 'student' and group_stud != None:
            __student_start(name_user, id_us_tg, group_stud)
        elif role == 'prepod' and group_stud == None:
            __prepod_start(name_user, id_us_tg)
    
    else:
        #update_us(id_us_tg)
        print(id_us_tg ,' ты уже зареган')
