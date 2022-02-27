import us_init

def poll_strat():
    pass


def student_start(name_user, id_us_tg,name_group):
    us_init.add_group(name_group, "true")
    us_init.add_student(name_user, id_us_tg, name_group)
    #us_init.start_gr(name_group)


def prepod_start(name_user, id_us_tg):
    us_init.add_prepod(name_user, id_us_tg)
    us_init.start_pr(name_user)


def reg_us(name_user, id_us_tg, role, group_stud = None):
    us_init.add_us(id_us_tg, role)

    if role == 'stud' and group_stud != None:
        student_start(name_user, id_us_tg, group_stud)
    elif role == 'prepod' and group_stud == None:
        prepod_start(name_user, id_us_tg)


if __name__ == '__main__':
    pass


