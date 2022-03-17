""" Система регистарции студентов, преподов, админов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import prep_text_pars

import all_con_bot_bd


all_groups = all_con_bot_bd.list_all_group()

# all_groups = ['М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19', 'М3О-118М-21', 'М3О-118М-21',
#               'М3О-111М-21', 'М3О-111М-21', 'М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19']
# for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
#     all_groups.append(data['group'])
#     print(data)


registerData = {}  # {*user_id*: {'user_role': *role*, 'user_group': *group*}}


class registerUser(StatesGroup):
    waiting_for_role = State()
    waiting_for_fio = State()
    waiting_for_group = State()


class register_change_group_fsm(StatesGroup):
    waiting_for_new_group = State()


class register_change_fio_fsm(StatesGroup):
    waiting_for_new_fio = State()


async def msgWithGroupName(message: types.Message):
    if message.text in all_groups:
        await message.answer('reply keyboard removed', reply_markup=types.ReplyKeyboardRemove())


async def already_registered(message: types.Message, state: FSMContext):

    if all_con_bot_bd.find_role_us(tg_id=message.chat.id) == 'student':
        await message.answer('Данные обновлены: ' + '\nВы: ' + all_con_bot_bd.find_fio_us(message.chat.id) + '; ' + 'Ваша группа: ' + all_con_bot_bd.find_group_us(message.chat.id) +' Ваша роль: ' + all_con_bot_bd.find_group_us(message.chat.id), reply_markup=types.ReplyKeyboardRemove())

    elif all_con_bot_bd.find_role_us(tg_id=message.chat.id) == 'prepod':
        await message.answer('Вы уже зарегистрированы' + '\nВы: ' + str(registerData[message.chat.id]['chosen_fio']) + '; ' + 'Ваша роль: ' + str(registerData[message.chat.id]['chosen_role']), reply_markup=types.ReplyKeyboardRemove())

    buttons = [
        types.InlineKeyboardButton(
            text="Да", callback_data="register_change_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="register_change_false")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer('Хотите изменить рег. данные?', reply_markup=keyboard)


async def choose_role(message: types.Message):

    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="is_student"),
        types.InlineKeyboardButton(
            text="Преподаватель", callback_data="is_prepod"),
        types.InlineKeyboardButton(
            text="Админ", callback_data="is_admin")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите роль      ", reply_markup=keyboard)


async def choose_fio(message: types.Message, state: FSMContext):
    fio = message.text
    await state.update_data(chosen_fio=fio)
    user_data = await state.get_data()
    if user_data['chosen_role'] == 'student':
        marakap = ReplyKeyboardMarkup(one_time_keyboard=True)

        for data in all_groups:
            marakap.add(KeyboardButton(data))

        await message.reply('Выберите группу', reply_markup=marakap)
        await registerUser.waiting_for_group.set()

    else:

        # ############### БРАТЬ ДАННЫЕ О РЕГИСТРАЦИИ ПРЕПОДА ТУТ ##########

        await message.reply('Ваше ФИО: ' + user_data['chosen_fio'] + '; Ваша роль: ' + user_data['chosen_role'])

        registerData[message.chat.id] = {'chosen_fio': user_data['chosen_fio'],
                                         'chosen_group': 'prepod', 'chosen_role': user_data['chosen_role']}

        all_con_bot_bd.add_prepod(fio=user_data['chosen_fio'], rg_id=message.chat.id, role=user_data['chosen_role'])

        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())

        await state.finish()


async def wrong_group(message: types.Message):
    return await message.reply('Выберите группу из списка')


async def choose_group(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['chosen_role'] == "student":

        group = message.text

        await state.update_data(chosen_group=group)
        user_data = await state.get_data()
        await message.answer('Ваше ФИО: ' + user_data['chosen_fio'] + '; Ваша группа: ' + user_data['chosen_group'] + '; Ваша роль: ' + user_data['chosen_role'], reply_markup=types.ReplyKeyboardRemove())

        registerData[message.chat.id] = {'chosen_fio': user_data['chosen_fio'],
                                         'chosen_group': user_data['chosen_group'], 'chosen_role': user_data['chosen_role']}

        all_con_bot_bd.add_st(fio=user_data['chosen_fio'], tg_id=message.chat.id, role=user_data['chosen_role'], group=user_data['chosen_group'])

        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def register_change_true(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# ДОБАВИТЬ ПРОВЕРКУ НА ПРЕПА/СТУДЕНТА

    if registerData[call.message.chat.id]['chosen_role'] == 'student':
        buttons = [
            types.InlineKeyboardButton(
                text="ФИО", callback_data="register_change_fio"),
            types.InlineKeyboardButton(
                text="Группу", callback_data="register_change_group")
        ]

    elif registerData[call.message.chat.id]['chosen_role'] == 'prepod':
        buttons = [
            types.InlineKeyboardButton(
                text="ФИО", callback_data="register_change_fio"),
        ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer('Что именно изменить?', reply_markup=keyboard)


async def register_change_false(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('Окес, ничего не меняем')


# register_change_fio_fsm.waiting_for_new_fio
async def register_change_fio_set_fio(message: types.Message, state: FSMContext):
    new_fio = message.text
    registerData[message.chat.id]['chosen_fio'] = new_fio

    all_con_bot_bd.update_data_user(role=registerData[message.chat.id]['chosen_role'], command='name', new_data=registerData[message.chat.id]['chosen_fio'], id_us_tg=message.chat.id)
    
    await state.finish()
    if registerData[message.chat.id]['chosen_role'] == 'student':
        await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData[message.chat.id]['chosen_fio']) + '; ' + 'Ваша группа: ' + str(registerData[message.chat.id]['chosen_group']+' Ваша роль: ' + str(registerData[message.chat.id]['chosen_role'])), reply_markup=types.ReplyKeyboardRemove())

    elif registerData[message.chat.id]['chosen_role'] == 'prepod':
        await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData[message.chat.id]['chosen_fio']) + '; ' + 'Ваша роль: ' + str(registerData[message.chat.id]['chosen_role']), reply_markup=types.ReplyKeyboardRemove())


# register_change_group_fsm.waiting_for_new_group
async def register_change_group_set_group(message: types.Message, state: FSMContext):
    new_group = message.text
    registerData[message.chat.id]['chosen_group'] = new_group

    all_con_bot_bd.update_data_user(role=registerData[message.chat.id]['chosen_role'], command='group', new_data=registerData[message.chat.id]['chosen_group'], id_us_tg=message.chat.id)

    await state.finish()
    if registerData[message.chat.id]['chosen_role'] == 'student':
        await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData[message.chat.id]['chosen_fio']) + '; ' + 'Ваша группа: ' + str(registerData[message.chat.id]['chosen_group']+' Ваша роль: ' + str(registerData[message.chat.id]['chosen_role'])), reply_markup=types.ReplyKeyboardRemove())


async def register_change_fio(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await register_change_fio_fsm.waiting_for_new_fio.set()
    await call.message.answer('Введите новые ФИО')


async def register_change_group(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    # сделать изменения в бд и проверку, есть ли уже такое
    marakap = ReplyKeyboardMarkup(one_time_keyboard=True)
    for data in all_groups:
        marakap.add(KeyboardButton(data))

    await register_change_group_fsm.waiting_for_new_group.set()
    await call.message.answer('Выберите группу', reply_markup=marakap)


async def is_student(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="student")
    await call.message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()


async def is_prepod(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="prepod")

    await call.message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()


async def is_admin(call: types.CallbackQuery):
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    print(call.from_user)
    await call.message.answer('user ' + str(call.from_user.id) + ' tryin 2 becum admin')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(
        already_registered, lambda message: all_con_bot_bd.check_valid_us(message.chat.id), commands='register')

    dp.register_message_handler(choose_role, commands="register", state="*")
    dp.register_message_handler(choose_fio, state=registerUser.waiting_for_fio)
    dp.register_message_handler(
        choose_group, lambda message: message.text in all_groups, state=registerUser.waiting_for_group)

    dp.register_message_handler(
        wrong_group, lambda message: message.text not in all_groups, state=registerUser.waiting_for_group)

    dp.register_message_handler(
        register_change_group_set_group, lambda message: message.text in all_groups, state=register_change_group_fsm.waiting_for_new_group)

    dp.register_message_handler(
        wrong_group, lambda message: message.text not in all_groups, state=register_change_group_fsm.waiting_for_new_group)

    dp.register_message_handler(
        register_change_fio_set_fio, state=register_change_fio_fsm.waiting_for_new_fio)


    dp.register_message_handler(cancel_handler, commands="cancel", state="*")

    dp.register_callback_query_handler(
        register_change_true, text="register_change_true")
    dp.register_callback_query_handler(
        register_change_false, text="register_change_false")
    dp.register_callback_query_handler(
        register_change_fio, text="register_change_fio")
    dp.register_callback_query_handler(
        register_change_group, text="register_change_group")

    dp.register_callback_query_handler(is_student, text="is_student")
    dp.register_callback_query_handler(is_prepod, text="is_prepod")
    dp.register_callback_query_handler(is_admin, text="is_admin")

    dp.register_message_handler(msgWithGroupName)
