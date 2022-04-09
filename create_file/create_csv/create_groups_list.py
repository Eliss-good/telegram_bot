import os
import openpyxl
from random import randint
from datetime import datetime

NAME_FILE: str = 'groups_list.xlsx'

def create_name_file():
    now = datetime.now()
    name = 'up_groups_' + str(randint(5000, 10000)) + '_' + now.strftime("%d/%m/%Y_%H:%M:%S") + '.xlsx'

    return name

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

    book.save(os.getcwd() + '/'+ NAME_FILE)
    book.close()

    return os.getcwd() + '/' + NAME_FILE
