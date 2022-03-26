def search_form_id_json(new_answers):
    for one_answer in new_answers:
        for about_one_answer in new_answers[one_answer]:
            try:
                print(about_one_answer)
                return int(about_one_answer["unique_form_id"])
            except KeyError:
                print("ERORR БЛЯЯТЬ", search_answer_in_json.__name__)

def search_answer_in_json(new_answers):
   """Форматирование json результатов опроса"""
   result_answers = {}

   for one_answer in new_answers:
      for about_one_answer in new_answers[one_answer]:
         for name_res, res in about_one_answer.items():
            if name_res == "pollAnswer":
                print(res)
                res_nums_answer = res["option_ids"]
                for item in res_nums_answer:
                    res_str_answer = about_one_answer["pollCopy"]["options"][int(item)]
                    result_answers[res_str_answer] = about_one_answer["pollCopy"]["question"]
            elif name_res == "messageAnswer":
               res_str_answer = str(res['text'])
               result_answers[res_str_answer] = about_one_answer["messageCopy"]["question"]

   return result_answers