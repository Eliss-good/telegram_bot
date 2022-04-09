import os
import openpyxl
from random import randint
from datetime import datetime

def create_name_file():
    now = datetime.now()
    name = 'up_groups_' + str(randint(5000, 10000)) + '_' + now.strftime("%d_%m_%Y___%H_%M_%S") + '.xlsx'
    directory = os.getcwd() + "/create_file/create_csv/athive/" + name

    return directory

def create_file_group(uploaded_groups: dict):
    new_name = create_name_file()
    book = openpyxl.Workbook()

    sheet = book.active
    sheet['Z100'] = ' '
    column: int = 0
    for group in uploaded_groups:
        sheet[1][column].value = group

        row: int = 2
        for one_people in uploaded_groups[group]:
            sheet[row][column].value = one_people
            row += 1
        row = 1
        column += 1

    book.save(new_name)
    book.close()

    return new_name
