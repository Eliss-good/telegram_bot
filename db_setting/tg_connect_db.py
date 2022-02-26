import us_init

def student_start(fio ,name_group, id_us_tg):
    name_group = us_init.correct_str(name_group)
    fio = us_init.correct_str(fio)
    id_us_tg= us_init.correct_str(str(id_us_tg))


    us_init.add_group(name_group, "'true'")
    us_init.add_us(id_us_tg)
    us_init.add_student(fio, id_us_tg, name_group)
    us_init.start_gr(name_group)

    
if __name__ == '__main__':
    pass


