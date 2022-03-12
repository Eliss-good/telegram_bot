""" Система регистарции студентов, преподов, админов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import prep_text_pars


all_groups = []
for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
    all_groups.append(data['group'])


class registerUser(StatesGroup):
    waiting_for_role = State()
    waiting_for_fio = State()
    waiting_for_group = State()


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

        # await message.reply('вы ' + user_data['chosen_fio'] + ' ' + user_data['chosen_role'])
        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())

        # ######################### ############### ##########
        await state.finish()


async def wrong_group(message: types.Message):
    return await message.reply('Выберите группу из списка')


async def choose_group(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['chosen_role'] != "prepod":

        group = message.text

        await state.update_data(chosen_group=group)
        user_data = await state.get_data()
        # await message.answer(f"{user_data['chosen_role']} {user_data['chosen_group']} {user_data['chosen_fio']}.\n", reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def register_change_true(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# ДОБАВИТЬ ПРОВЕРКУ НА ПРЕПА/СТУДЕНТА

    buttons = [
        types.InlineKeyboardButton(
            text="ФИО", callback_data="register_change_fio"),
        types.InlineKeyboardButton(
            text="Группу", callback_data="register_change_group")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer('Что именно изменить?', reply_markup=keyboard)


async def register_change_false(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('Окес')


async def register_change_fio(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# сделать изменения в бд и проверку, есть ли уже такое

    await call.message.answer('фио изменено')


async def register_change_group(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# сделать изменения в бд и проверку, есть ли уже такое

    await call.message.answer('группа изменена')


async def is_student(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="student")
    await call.answer()
    await call.message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()


async def is_prepod(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="prepod")
    await call.answer()
    await call.message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()


async def is_admin(call: types.CallbackQuery):
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
    dp.register_message_handler(choose_role, commands="register", state="*")
    dp.register_message_handler(choose_fio, state=registerUser.waiting_for_fio)
    dp.register_message_handler(
        choose_group, state=registerUser.waiting_for_group)

    dp.register_message_handler(
        wrong_group, lambda message: message.text not in all_groups, state=registerUser.waiting_for_group)

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
