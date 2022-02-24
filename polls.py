from aiogram import types, Bot

async def cmd_poll(self, message: types.Message):
    
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    chat_id = '@KremlynBot'
    is_anonymous = True
    open_period = 60
    question = 'you are'
    poll = await Bot.send_poll(self, options=options, is_anonymous=is_anonymous, open_period=open_period, question=question)
    