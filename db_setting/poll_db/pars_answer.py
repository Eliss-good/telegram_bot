def search_form_id_json(new_answers):
    for one_answer in new_answers:
        for about_one_answer in new_answers[one_answer]:
            try:
                print(about_one_answer)
                return int(about_one_answer["unique_form_id"])
            except KeyError:
                print("ERROR fun", search_answer_in_json.__name__)


def tg_id_answer_is_json(new_anwers):
    users = []
    for tg_id in  new_anwers:
        users.append(tg_id)

    return users


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
                    result_answers[about_one_answer["pollCopy"]["question"]] = res_str_answer
            elif name_res == "messageAnswer":
               res_str_answer = str(res['text'])
               result_answers[about_one_answer["messageCopy"]["question"]] = res_str_answer

   return result_answers