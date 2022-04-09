import db_setting.back_function_db as bf
import db_setting.poll_db.pars_answer as prs_an
import json


def read_answer_to_file():
   """Чтение файла с ответами"""
   all_ansver_json = []

   with open("all_answer.json", "r", encoding='utf-8') as data_file:
         all_ansver_json = json.load(data_file)
   return all_ansver_json


def write_answer_to_file(all_survay_json):
   """Запись в файл"""
   with open("all_answer.json", "w", encoding='utf-8') as data_file:
      json.dump(all_survay_json, data_file, ensure_ascii=False, indent=4)


def add_to_sub_form(form_id: int, groups: list):
   """Добавление к form_id список групп"""
   all_form = read_answer_to_file()

   try:
      for one_group in groups:
         all_form[bf.find_id_survay(form_id)]['send_group'].append(one_group)
      write_answer_to_file(all_form)
   except:
      print('not find this form')


def find_groups_is_form(survey_id: int):
   """Возвращает все группы, которым отправлена форма"""
   all_answer = read_answer_to_file()

   try:
      return all_answer[str(survey_id)]['send_groups']
   except:
      print("ERROR fun", find_groups_is_form.__name__)
      return []



def all_groups_form(groups: list, form_id: int):
   """Добавление групп которым отправлена форма"""
   form_data = read_answer_to_file()
   id_survey = str(bf.find_id_survay(form_id))

   if id_survey:
      try:
         for one_group in groups:
            form_data[id_survey]['send_group'].append(one_group)

         write_answer_to_file(form_data)
      except:
         print("ERROR fun", all_groups_form.__name__)



def all_users_send_form(users_tg: list, form_id: int):
   """Добавление пользователей которым отправлена форма"""
   form_data = read_answer_to_file()
   id_survey = str(bf.find_id_survay(form_id))

   if id_survey:
      try:
         for one_us in users_tg:
            form_data[id_survey]['send_users'].append(one_us)
         
         write_answer_to_file(form_data)
      except:
         print("ERROR fun", all_users_send_form.__name__)
         


def add_answer_tg_us(form_data: dict, survey_id: int ,tg_id: int):
   """Добавление пользователя, который проголосовал"""
   form_data[str(survey_id)]['user_replied'].append(tg_id)
   return form_data


def add_answer_for_survay(new_answer):
   """Добавление новых ответов"""
   form_id = prs_an.search_form_id_json(new_answer)
   result_answer = prs_an.search_answer_in_json(new_answer)
   data_file = read_answer_to_file()

   survay_id = str(bf.find_id_survay(form_id))
   tg_id = prs_an.tg_id_answer_is_json(new_answer)


   try:
      data_file[survay_id]['all_answer'].append(result_answer)
      data_file = add_answer_tg_us(data_file, survay_id, tg_id[0])
      write_answer_to_file(data_file)

      print("Успещно добавлен ответ на опрос id:", form_id)
   except KeyError:
      print('Not find key into json file')


def update_group_in_survay(max_index_g, form_id):
   """Прикрепление к форме группу вопросов"""
   bf.db.update_db('survay_tb', ['groupquestion_id'], [max_index_g], ['form_id'], [form_id])


def create_group_question(dict_question : dict, form_id : int):
   """Создание новой группы вопросов для формы"""
   max_index_g = bf.max_index_group_question()
   max_index_g = str(max_index_g + 1)

   update_group_in_survay(max_index_g, str(form_id))
   for type_ques, ques in dict_question.items():
      for one_ques in ques:
         bf.add_group_questions(one_ques, max_index_g)


def _start_answer(data_survay):
   """Адаптирование новой формы из ТГ к форме json файла"""

   ########## create form answer ###########
   new_file = {}
   new_file['info_form'] = data_survay
   new_file['send_group'] = []
   new_file['send_users'] = []
   new_file['user_replied'] = []
   new_file['questions'] = {}
   new_file['all_answer'] = []
   #########################################

   for item in data_survay[:-1]:
      try:
         if new_file['questions'].get(item['type']) == None:
            new_file['questions'][item['type']] = []

         new_file['questions'][item['type']].append(item['question'])

         bf.add_questions(item['question'])
      except:
         print("ERROR fun", _start_answer.__name__)
   
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
