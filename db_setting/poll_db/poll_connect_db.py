import back_function_db as bf
import json

path = '/home/eliss/ptoject/telegram_bot/db_setting/polls_answer'

def read_answer_to_file():
   all_ansver_json = []

   with open( "all_answer.json", "r", encoding='utf-8') as data_file:
         all_ansver_json = json.load(data_file)

   return all_ansver_json


def write_answer_to_file(all_survay_json):
   with open("all_answer.json", "w", encoding='utf-8') as data_file:
      json.dump(all_survay_json, data_file, indent=4)


def update_group_in_survay(max_index_g, survay_code):
   bf.db.update_db('survay_tb', ['groupquestion_id'], [max_index_g], ['survay_code'], [survay_code])
   

def add_answer_for_survay(new_result_answer):
####определить приход хеша
   survay_code = 1
   data_file = read_answer_to_file()

   try:
      data_file[str(bf.find_id_survay(survay_code))]['answer'].append(new_result_answer)
   except KeyError:
      print('Not find key into json file')
      return
   
   write_answer_to_file(data_file)


def create_group_question(list_question, survay_code):
   max_index_g = bf.max_index_group_question()
   max_index_g = str(max_index_g + 1)

   update_group_in_survay(max_index_g, str(survay_code))
   for quest in list_question:
      bf.add_group_questions(quest, max_index_g)

   
def _start_answer(data_survay, from_id):
   """Адаптирование новой формы из ТГ к форме json файла"""
   print(list(data_survay.keys())[0])
   from_tg_data = data_survay[list(data_survay.keys())[0]]
   
   ########## create form answer ###########
   new_file = {}
   new_file['survay_code'] = int(list(data_survay.keys())[0])
   new_file['survey_name'] = from_tg_data[-1]['form_name']
   new_file['from_teleg_id'] = from_id
   new_file['questions'] = []
   new_file['answer'] = []
   #########################################
   
   for item in range (len(from_tg_data) - 1):
      new_file['questions'].append(from_tg_data[item]['question'])
      bf.add_questions(from_tg_data[item]['question'])
   
   create_group_question(new_file['questions'], int(list(data_survay.keys())[0]))

   return new_file


##### add into DBase new survay #####
def add_survay(from_id, to_group, data_survay):
   """Добавление новой формы"""

   from_tg_data = data_survay[list(data_survay.keys())[0]]
   poll_ck  = bf.db.select_db_where('survay_tb', ['id'], ['survay_code'], [int(list(data_survay.keys())[0])], 'check')

   if poll_ck:
      new_data = [(list(data_survay.keys())[0]), bf.correct_str(from_tg_data[-1]['form_name']), bf.correct_str(str(from_id)), bf.correct_str(str(to_group))]
      bf.db.insert_db('survay_tb', ['survay_code','survay_name', 'from_id', 'to_group'], new_data)

      all_survay_json = read_answer_to_file() 
      try:
         all_survay_json[bf.find_id_survay(int(list(data_survay.keys())[0]))]  = _start_answer(data_survay, from_id)
      except IndexError:
         print("bad insert json")
      write_answer_to_file(all_survay_json)

"""
with open(path + "/tg_result_poll.json", "r", encoding='utf-8') as file:
   data = json.load(file)
   add_survay(3, "М3О-212Б-20", data)
"""