""" Меню для системы опросов"""
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


from bot_elements.forms import mem_for_created_forms
# check forms mass and select user_ids + send forms in forms.py

async def display_current_mem_status(message: types.Message):
    full_message = ""
    form_number = 0
    for index in mem_for_created_forms:
        
        if mem_for_created_forms[index][-1]['creator_id'] == message.chat.id:
            selected_form = mem_for_created_forms[index]
            form_mem = selected_form
            print('form_mem ', form_mem)
            info = selected_form[-1]
            print('recip_mem ', info)
            
            parsed_msg = "\n ----- \nname: " + info['form_name'] + ' '+ 'form_id: ' + str(info['form_id']) + ' /send' + str(form_number) + "\n"
            form_number += 1
            if form_mem:
                
                for inside_mem in form_mem:
                    if inside_mem['type'] == 'poll':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                            str(e) for e in inside_mem['options']) + ']' + '\n')

                    elif inside_mem['type'] == 'msg':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + '\n')

        full_message += parsed_msg
    
    await message.answer(full_message)

def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
