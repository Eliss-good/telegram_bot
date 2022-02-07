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
  
    options = ['snaipa','pyro','demomen']
    await bot.send_poll(chat_id=message.chat.id, question='GOLOSOVANIJE', is_anonymous=False, options=options)
    


@dp.message_handler()
async def echo(message: types.Message):
    
    await message.answer("i jst aswr everythin")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
