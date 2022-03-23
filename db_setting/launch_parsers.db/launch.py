import back_function_db as bf
from .. import full_pars as fl

#####  pars for  group  #####
def setter_group_bd(name_group,t_item):
    """Заполнение бызы данных по группе"""
    bf.add_lesson(t_item['lesson'])
    bf.add_prepod(t_item['prepod'], 1)

    bf.connect_gr_th(name_group,t_item)


def start_gr(name_group):
    """Получение данных c парсера о группе"""
    data_result = fl.parse_group(name_group.upper())
    bf.add_group(name_group, True)

    for item in data_result:
        setter_group_bd(name_group, item)


##### pars for prepod #####
def data_for_prepod(t_item):
    """Заполнение бызы данных по ФИО препода"""
    bf.add_group(t_item['group'])
    bf.add_lesson(t_item['lesson'])
    
    bf.connect_gr_th(t_item['group'], t_item)


def start_pr(name_prepod):
    """Получение данных с препода по ФИО препода"""
    data = fl.parse_prepod(name_prepod)
    print(data)
    for item in data:
        data_for_prepod(item)
