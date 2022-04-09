from importlib.machinery import all_suffixes
from bots import admin_bot
from aiogram import types, Dispatcher
from bot_elements.admin_tools.displays import display_all_groups
from transliterate import translit

from bot_elements.getter.all_getters import get_fio_in_group

async def get_student_list_pdf(message: types.Message):
    group = message.text[18:].replace('_', '-') # получает ггуппу
    group_ru = translit(group, 'ru')

    all_fio = get_fio_in_group(group_ru)
    

    # здесь пропиши путь к сгенерированному файлу
    
    await message.answer(all_fio)


def register_handlers_get_data(dp: Dispatcher):
    dp.register_message_handler(
        display_all_groups, commands='get_student_list')
    dp.register_message_handler(
        get_student_list_pdf, lambda message: message.text.startswith('/get_student_list_'))