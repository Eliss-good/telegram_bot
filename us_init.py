from db_connect import DataConnect
import full_pars
import re

db = DataConnect()

"""def init_group_less(name_group):

    data = full_pars.parse_group(name_group)
    set_data = []

    status = True
    for item in data:
        for u_item in set_data:
            if item['prepod'] == u_item['prepod'] and item['lesson'] == u_item['lesson']:
                status = False
                break     
        
        if status:
            set_data.append(item)
        else:
            status = True

    print(set_data) """

def cheack_data(t_item):
    t_item['lesson'] = "'" + t_item['lesson'] + "'"
    t_item['prepod'] = "'" + t_item['prepod'] + "'"
    lesson_ck = db.cheack_data_bd('lesson_tb', ["id"], ['lesson_name'] ,[t_item['lesson']])
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [t_item['lesson']])
    
    con_data = [t_item['prepod'], str(db.select_db('lesson_tb', ['id'], add_com = ' where lesson_name = ' +  t_item['lesson'])[0][0])]
    if db.cheack_data_bd('teach_tb', ['id'], ['teach_name', 'lesson_id'], con_data):
        print('signal')
        db.custom_insert(com = "insert into teach_tb (teach_name, lesson_id) values (" + t_item['prepod'] + ", "
        + str(db.select_db('lesson_tb', ['id'], add_com = ' where lesson_name = ' +  t_item['lesson'])[0][0]) + ')')
    


def pars_data_for_gp(name_group):
    name_group = name_group.replace("'", '')
    print(name_group)
    data = full_pars.parse_group(name_group)
    print(data)
    
    for item in data:
        print('++')
        cheack_data(item)
        

def add_group(name_group):
    if db.cheack_data_bd('group_tb', ['id'], ['group_name']  ,[name_group]):
        db.insert_db('group_tb', ['group_name'] , [name_group])
    
    pars_data_for_gp(name_group)

add_group("'М3О-212Б-20'")

        
