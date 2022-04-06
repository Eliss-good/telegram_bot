import aiogram
from bots import admin_bot
from aiogram import types, Dispatcher
from transliterate import translit

async def display_all_groups(message: types.Message):
    group_list = ['М3О-221Б-20', 'М3О-212Б-20'] # тут получаем группы
    full_text = ''
    for group in group_list:
        full_text += str(group) + ' /get_student_list_' + str(translit(str(group), reversed=True)).replace('-', '_') + '\n'
    await message.answer(full_text)
