""" Меню для системы опросов"""
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from bot_elements.getter.all_getters import mem_for_created_forms_get_creator_id, mem_for_created_forms_get_data

from bot_elements.register import registerData
from bot_elements.setter.all_setters import send_forms_mem_add_sent_form

unique_sent_form_id = 0

from bot_elements.forms import mem_for_created_forms, send_forms_mem
# check forms mass and select user_ids + send forms in forms.py

async def display_current_mem_status(message: types.Message):
    full_message = ""
    for index in mem_for_created_forms:
        
        print(mem_for_created_forms_get_creator_id(form_id=index))

        if mem_for_created_forms_get_creator_id(form_id=index) == message.chat.id:
            selected_form = mem_for_created_forms_get_data(form_id=index)
            form_mem = selected_form
            print('form_mem ', form_mem)
            info = selected_form[-1]
            print('recip_mem ', info)
            
            parsed_msg = "\n ----- \nname: " + info['form_name'] + ' '+ 'form_id: ' + str(info['form_id']) + ' /send' + '_' + str(index) + "\n"

            if form_mem:
                
                for inside_mem in form_mem:
                    if inside_mem['type'] == 'poll':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                            str(e) for e in inside_mem['options']) + ']' + '\n')

                    elif inside_mem['type'] == 'msg':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + '\n')

            full_message += parsed_msg
    
    await message.answer(full_message, reply_markup=None)


#send fsm

class sender(StatesGroup):
    waiting_for_groups = State()


async def choose_group(message: types.Message, state: FSMContext):
    form_index = message.text[6:]

    await state.update_data(form_index=form_index)
    # await message.reply('Напишите через запятую группы-получатели')
    
    marakap = ReplyKeyboardMarkup(one_time_keyboard=True)
    for key in registerData:
        marakap.add(KeyboardButton(registerData[key]['chosen_fio'] + '; id ' + str(key)))

    await message.reply('Выберите получателя', reply_markup=marakap)
    await sender.waiting_for_groups.set()


async def sending(message: types.Message, state: FSMContext):
    global unique_sent_form_id
    send_to_user = int(message.text[(message.text.find('id ') + 3):])
    print(send_to_user)
    groups = message.text.split(',')
    final_data = await state.get_data()
    form_creator_user_id = mem_for_created_forms_get_creator_id(int(final_data['form_index']))
    # получить id юзеров по группам
    send_forms_mem_add_sent_form(form_id=int(final_data['form_index']), sent_form_id=unique_sent_form_id, form_creator_user_id=form_creator_user_id, send_to_users_ids=[send_to_user])
    
    print(send_forms_mem)

    unique_sent_form_id += 1

    await message.answer('Отправлено юзеру ' + ''.join(str(groups)), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
    dp.register_message_handler(choose_group, lambda message: message.text.startswith('/send'))
    dp.register_message_handler(sending, state=sender.waiting_for_groups)
