
import aiogram
from bots import admin_bot
from aiogram import types, Dispatcher
from transliterate import translit
from bot_elements.getter.all_getters import get_all_groups

async def display_all_groups(message: types.Message):
    group_list = get_all_groups() # тут получаем группы
    full_text = ''
    for group in group_list:
        full_text += str(group) + ' /get_student_list_' + str(translit(str(group), reversed=True)).replace('-', '_') + '\n'
    await message.answer(full_text)