from aiogram import Bot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

prepod_bot = Bot(token=config['DEFAULT']['prepodBotToken'])
student_bot = Bot(token=config['DEFAULT']['studentBotToken'])
admin_bot = Bot(token=config['DEFAULT']['adminBotToken'])