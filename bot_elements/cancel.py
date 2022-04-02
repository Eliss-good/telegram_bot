from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot_elements.remover.all_removers import temp_mem_for_form_creator_remove_form, completing_forms_dispatcher_remove_session

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        temp_mem_for_form_creator_remove_form(user_id=message.chat.id)
        completing_forms_dispatcher_remove_session(user_id=message.chat.id)
        await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
        return

    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_cancel(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, commands="cancel", state="*")
