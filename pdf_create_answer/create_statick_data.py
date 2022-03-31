import json

#from db_setting.poll_db.poll_connect_db import read_answer_to_file


def calculate_answer(form: dict, answer: str):
    """Подсчитывают ответы"""
    if form.get(answer) != None:
        form[answer] += 1
    else:
        try:
            form[answer] = 1
        except:
            print("ERROR : In counting responses")


def formatting_answer(form: dict):
    """Форматирует ответы"""
    result = {}
    for type_survey in form["questions"]:
        for one_ques in form["questions"][type_survey]:
            one_result = {"!!type!!" : type_survey}
            for one_answer in form["all_answer"]:
                if one_answer == "!!type!!":
                    continue
                calculate_answer(one_result, one_answer[one_ques])

            result[one_ques] = one_result

    return result

"""
def find_survay(survay_id : str):
    #Ищет в json файле нужный опрос, а потом и отаветы
    about_form = read_answer_to_file()[survay_id]
    return formatting_answer()
"""

with open('all_answer.json', 'r') as file:
    hey = json.load(file)
    print(formatting_answer(hey))