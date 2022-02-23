from db_connect import DataConnect
import full_pars as fl
import json

db = DataConnect()

def correct_str(t_item):
    t_item = "'" + t_item +"'" 
    return t_item 


def add_lesson(name_lesson):
    lesson_ck = db.select_db_where('lesson_tb', ['id'], ['lesson_name'] ,[name_lesson],'check')
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [name_lesson])


def add_prepod(name_prepod):
    prepod_ck = db.select_db_where('teach_tb', ['id'], ['teach_name'], [name_prepod], 'check')
    if prepod_ck:
        db.insert_db('teach_tb', ['teach_name'], [name_prepod])


def add_group(name_group, status):
    if db.select_db_where('group_tb', ['id'], ['group_name', 'group_approved']  ,[name_group, status], 'check'):
        db.insert_db('group_tb', ['group_name', 'group_approved'] , [name_group, status])


def add_group_from_json():
    with open('approved_group.json','r', encoding='utf-8') as file:
        apr_group = json.load(file)

        for item in apr_group:
            print(item)
            add_group(correct_str(item), str(apr_group[item]))
        

def find_id_group(name_group):
    return str(db.select_db_where('group_tb', ['id'], ['group_name'], [name_group], 'where')[0][0])


def find_id_global(name_teleg):
    return str(db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [name_teleg], 'where')[0][0])


def find_id_lesson(name_lesson):
    return str(db.select_db_where('lesson_tb', ['id'], ['lesson_name'], [name_lesson], 'where')[0][0])


def find_id_teach(name_teach):
    return str(db.select_db_where('teach_tb', ['id'], ['teach_name'], [name_teach], 'where')[0][0])



def connect_gr_th(name_group, t_item):
    con_data = [find_id_group(name_group), find_id_teach(t_item['prepod']), find_id_lesson(t_item['lesson']), t_item['role']]

    if db.select_db_where('connect_tb', ['id'], ['group_id','teach_id', 'lesson_id', 'teach_role'], con_data, 'check'):
        db.insert_db('connect_tb', ['group_id','teach_id', 'lesson_id', 'teach_role'], con_data)
    
def check_data_for_group(name_group,t_item):
    t_item['lesson'] = correct_str(t_item['lesson'])
    t_item['prepod'] = correct_str(t_item['prepod'])
    t_item['role'] = correct_str(t_item['role'])


    add_lesson(t_item['lesson'])
    add_prepod(t_item['prepod'])

    connect_gr_th(name_group,t_item)

def start_gr(name_group):
    data = fl.parse_group(name_group)
    name_group = correct_str(name_group)

    for item in data:
        check_data_for_group(name_group, item)
        
start_gr('М3О-221Б-20')