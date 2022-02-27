import us_init
import json


def _group_cheack_approved(name_group):
    with open('approved_group.json','r', encoding='utf-8') as file:
        apr_group = json.load(file)

        try:
            status = apr_group[name_group]
            return status
        except KeyError:
            return False


def jump_group_prepod(name_prepod):
    data = us_init.fl.parse_prepod(name_prepod)

    for item in data:
        us_init.data_for_prepod(item)


def student_start(name_user, id_us_tg,name_group):
    us_init.add_group(name_group, "true")
    us_init.add_student(name_user, id_us_tg, name_group)
    #us_init.start_gr(name_group)


def prepod_start(name_user, id_us_tg):
    us_init.add_prepod(name_user, id_us_tg)
    
    

    

def reg_us(name_user, id_us_tg, role, group_stud = None):
    us_init.add_us(id_us_tg, role)

    if role == 'stud' and group_stud != None:
        student_start(name_user, id_us_tg, group_stud)
    elif role == 'prepod' and group_stud == None:
        prepod_start(name_user, id_us_tg)


if __name__ == '__main__':
    pass


