import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['poll'])
async def send_welcome(message: types.Message):
  
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    
    is_anonymous = True
    open_period = 60
    question = 'you are'
    poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, open_period=open_period, question=question, chat_id=message.chat.id)

@dp.message_handler()
async def echo(message: types.Message):
    
    await message.answer("i jst aswr everythin")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)