import db_setting.back_function_db as bf
import json


def read_answer_to_file():
   """Чтение файла с ответами"""
   all_ansver_json = []

   with open( "all_answer.json", "r", encoding='utf-8') as data_file:
         all_ansver_json = json.load(data_file)
   return all_ansver_json


def write_answer_to_file(all_survay_json):
   """Запись в файл"""
   with open("all_answer.json", "w", encoding='utf-8') as data_file:
      json.dump(all_survay_json, data_file, indent=4)


def add_to_sub_form(form_id, groups):
   all_form = read_answer_to_file()

   try:
      all_form[bf.find_id_survay(form_id)]['send_group'] = groups
      write_answer_to_file(all_form)
   except:
      print('not find this form')



def add_answer_for_survay(new_result_answer):
####определить приход хеша
   form_id = 1
   data_file = read_answer_to_file()

   try:
      data_file[str(bf.find_id_survay(form_id))]['answer'].append(new_result_answer)
   except KeyError:
      print('Not find key into json file')
      return
   
   write_answer_to_file(data_file)


def update_group_in_survay(max_index_g, form_id):
   bf.db.update_db('survay_tb', ['groupquestion_id'], [max_index_g], ['form_id'], [form_id])


def create_group_question(list_question, form_id):
   """Создание новой группы вопросов для формы"""
   max_index_g = bf.max_index_group_question()
   max_index_g = str(max_index_g + 1)

   update_group_in_survay(max_index_g, str(form_id))
   for quest in list_question:
      bf.add_group_questions(quest, max_index_g)


def _start_answer(data_survay):
   """Адаптирование новой формы из ТГ к форме json файла"""

   ########## create form answer ###########
   new_file = {}
   new_file['info_form'] = data_survay
   new_file['send_group'] = []
   new_file['questions'] = []
   new_file['all_answer'] = []
   #########################################

   print(data_survay[:-1])

   for item in data_survay[:-1]:
      new_file['questions'].append(item['question'])
      bf.add_questions(item['question'])
   
   create_group_question(new_file['questions'], data_survay[-1]['form_id'])
   return new_file



##### add into DBase new survay #####
def add_survay(data_survay):
   """Добавление новой формы"""
   poll_ck  = bf.db.select_db_where('survay_tb', ['id'], ['form_id'], [str(data_survay[-1]["form_id"])], 'check')

   if poll_ck:
      new_data = [str(data_survay[-1]['form_id']), bf.correct_str(data_survay[-1]['form_name']), bf.correct_str(str(data_survay[-1]['creator_id']))]
      bf.db.insert_db('survay_tb', ['form_id', 'form_name', 'from_id'], new_data)

      all_survay_json = read_answer_to_file() 
      try:
         all_survay_json[bf.find_id_survay(data_survay[-1]['form_id'])]  = _start_answer(data_survay)
      except IndexError:
         print("bad insert json")
      write_answer_to_file(all_survay_json)


with open("test_survay.json", "r", encoding='utf-8') as file:
   data = json.load(file)
   add_survay(data)

