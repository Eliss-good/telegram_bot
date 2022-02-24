from db_connect import DataConnect
#import us_init as u_in
import json


db = DataConnect()

#Для работы этого нужен парсер, после напишу
def check_prepod_group(prepod_name):
    """with open('approved_group.json','r', encoding='utf-8') as file:
        apr_group = json.load(file) """




def add_lesson(name_lesson):
    lesson_ck = db.cheack_data_bd('lesson_tb', ["id"], ['lesson_name'] ,[name_lesson])
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [name_lesson])

    return(lesson_ck)

def add_group():
    
    

def add_stud(obj_us):
    idor_data = [str(db.select_db('global_tb',['id'], add_com = ' where gl_teleg_id = ' + obj_us.teleg_id ))]
    group_status = db.select_db('group_tb',['id'], add_com = ' where group_name = ' + obj_us.group_name)[0][0]

    if group_status == None:
        #u_in.add_group(obj_us.group_name)
        group_status = db.select_db('group_tb',['id'], add_com = ' where group_name = ' + obj_us.group_name)[0][0]
    
    idor_data.append(group_status)
    db.insert_db('student_tb', ['gl_id','group_id'], idor_data)


def add_teach(obj_us):
    idor_data = [str(db.select_db('global_tb',['id'], add_com = ' where gl_teleg_id = ' + obj_us.teleg_id ))]
    


def check_us(obj_us):
    if db.cheack_data_bd('global_tb', ['id'], ['gl_teleg_id'], [obj_us.teleg_id]):
       db.insert_db('global_tb', ['gl_teleg_id', 'gl_role'], [obj_us.teleg_id, obj_us.role])

    if db.select_db('global_tb', ['gl_role'], add_com = 'where gl_teleg_id = ' + obj_us.teleg_id) != None:
        #функция update ещё не добавлена
        pass

    if obj_us.role == 'stud':
        add_stud(obj_us)
    elif obj_us.role == 'teach':
        add_teach(obj_us)
    
cheack_prepod_group('kok')

