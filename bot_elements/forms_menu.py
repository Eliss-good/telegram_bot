""" Меню для системы опросов"""
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand


from bot_elements.forms import mem_for_created_forms, send_forms_mem
# check forms mass and select user_ids + send forms in forms.py

async def display_current_mem_status(message: types.Message):
    full_message = ""
    for index in mem_for_created_forms:
        
        if mem_for_created_forms[index][-1]['creator_id'] == message.chat.id:
            selected_form = mem_for_created_forms[index]
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
    
    await message.answer(full_message)


#send fsm

class sender(StatesGroup):
    waiting_for_groups = State()


async def choose_group(message: types.Message, state: FSMContext):
    form_index = message.text[6:]

    await state.update_data(form_index=form_index)
    await message.reply('Напишите через запятую группы-получатели')
    await sender.waiting_for_groups.set()


async def sending(message: types.Message, state: FSMContext):
    groups = message.text.split(',')
    final_data = await state.get_data()
    form_creator_user_id = mem_for_created_forms[int(final_data['form_index'])][-1]['creator_id']
    # получить id юзеров по группам
    send_forms_mem.append({'form_id': int(final_data['form_index']), 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': [506629389]}})
    # print(send_forms_mem)
    await state.finish()


# async def activate_cycle(message: types.Message):
#     """ Получает название формы, добавляет данные в forms_dispatcher,
#         запускает отправку вопросов из нужной формы"""
    
#     selected_form = mem_for_created_forms[index]
#     send_id = int(message.text[5:])
#     print(selected_form[send_id])
#     form_name = str(message.text)[6:]
#     curr_form = {}
#     curr_form['user_id'] = message.chat.id
#     curr_form['form_name'] = form_name
#     forms_dispatcher.append(curr_form.copy())
#     curr_form.clear()

#     await go_cycle()


# # complete polls
# async def go_cycle():
#     """Отсылает вопросы/ опросы из forms_dispatcher"""

#     print(forms_dispatcher)
#     for curr_started_form in forms_dispatcher:
#         form_name = curr_started_form['form_name']

#         if multiple_polls_dispatcher:
#             for select_form in multiple_polls_dispatcher:
#                 if select_form[-1]['form_name'] == form_name:

#                     curr_quest = select_form[0]

#                     if curr_quest['type'] == 'poll':

#                         msg = await bot.send_poll(chat_id=curr_started_form['user_id'], question=curr_quest['question'], options=curr_quest['options'], is_anonymous=True)
#                         curr_quest['id'] = msg.poll.id

#                     elif curr_quest['type'] == 'msg':
#                         msg = await bot.send_message(chat_id=curr_started_form['user_id'], text=curr_quest['question'])
#                         curr_quest['id'] = msg.message_id
#                         # print(curr_quest['id'])

#                     elif curr_quest['type'] == 'info':
#                         multiple_polls_dispatcher[0].remove(
#                             {'form_name': curr_quest['form_name'], 'user_id': curr_quest['user_id'], 'type': 'info'})
#                         multiple_polls_dispatcher.pop(0)
#                         forms_dispatcher.remove(
#                             {'user_id': curr_started_form['user_id'], 'form_name': form_name})
#                         print('theend')


# def lambda_checker_poll(poll):
#     """Проверяет принадлежит ли опрос выбранной форме"""

#     for data in multiple_polls_dispatcher:
#         for a in data:
#             # print(a)
#             if a['id'] == poll['id']:
#                 data.remove(
#                     {'question': a['question'], 'options': a['options'], 'id': a['id'], 'type': 'poll'})
#                 # print('eh')
#                 return True
#     # print('folss')
#     return False


# def lambda_checker_msg(message: types.Message):
#     """Проверяет является ли сообщение ответом на вопрос из формы"""

#     for data in multiple_polls_dispatcher:
#         for a in data:
#             # ! проверить, не совпадают ли айдишники из разных чатов
#             if a['id'] + 1 == message.message_id:
#                 data.remove(
#                     {'question': a['question'], 'id': a['id'], 'type': 'msg'})
#                 # print('eh')
#                 # print(message.text)
#                 return True
#     # print('folss')
#     return False


# # handler activates when vote/send answer
# async def poll_handler(poll: types.PollAnswer):
#     """Активируется, когда приходит ответ на опрос/ опрос закрывается"""

#     print(poll)
#     if multiple_polls_dispatcher:
#         print('go ahead pol')
#         await go_cycle()
#     # print(poll['id'])


# async def msg_handlr(message: types.Message):
#     """Активируется, когда приходит сообщение"""

#     print(message)
#     if multiple_polls_dispatcher:
#         # print('go ahead msg')
#         await go_cycle()

    


def register_handlers_forms_menu(dp: Dispatcher):
    dp.register_message_handler(display_current_mem_status, commands="saved_forms", state="*")
    dp.register_message_handler(choose_group, lambda message: message.text.startswith('/send'))
    dp.register_message_handler(sending, state=sender.waiting_for_groups)