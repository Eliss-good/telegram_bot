from bot_elements.getter.all_getters import registerData_get
from bot_elements.setter.all_setters import registerData_accept_register, registerData_deny_register
from aiogram import types, Dispatcher
from bots import student_bot, admin_bot

async def display_unregistered_users(message: types.Message):
    """ Формат
      user_id :  {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role, 'confirmed': False}
    """
    registerData = registerData_get()
    if registerData:
        full_text = ''
        count = 1
        for user_id in registerData:
            
            selected_user_data = registerData[user_id]
            if selected_user_data['chosen_role'] == 'student':
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['chosen_fio']) + ' ГРУППА: ' + str(selected_user_data['chosen_group']) + ' РОЛЬ: ' + str(selected_user_data['chosen_role']) + ' /accept_' + str(user_id) + ' /deny_' + str(user_id) +'\n'
            
            elif selected_user_data['chosen_role'] == 'prepod':
                full_text += str(count) + ') ФИО: ' + str(selected_user_data['chosen_fio']) + ' РОЛЬ: ' + str(selected_user_data['chosen_role']) + ' /accept_' + str(user_id) + ' /deny_' + str(user_id) +'\n'
            
            count += 1
        await message.answer(full_text)
    else:
        await message.answer(' Нет неподтвержденных пользователей')


async def accept_register(message: types.Message):
    user_id = int(message.text[8:])
    await registerData_accept_register(user_id=user_id, message=message)
    

async def deny_register(message: types.Message):
    user_id = int(message.text[6:])
    await registerData_deny_register(user_id=user_id, message=message)
    

def register_handlers_forms_check_register(dp: Dispatcher):
    dp.register_message_handler(
        display_unregistered_users, commands='check_unregistered_users')
    
    dp.register_message_handler(accept_register, lambda message: message.text.startswith('/accept_'))
    dp.register_message_handler(deny_register, lambda message: message.text.startswith('/deny_'))
