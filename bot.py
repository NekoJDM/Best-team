import telebot
from telebot import types
from gh_menu import gh_menu
import db_users
from config import create_menu, Goods
import config

bot = telebot.TeleBot(config.TOKEN)

text_messages = {
	'start':
		u'Приветствую тебя, {name}!\n'
		u'Я помогу тебе сделать онлайн заказ (это быстро и без очереди).\n\n'
		u'1. Выбери интересующий напиток/сэндвич/десерт (Ты можешь выбрать несколько)\n'
		u'2. Выбери время, когда захочешь забрать заказ\n'
		u'3. Оплати заказ (это безопасно)\n'
		u'4. Обязательно забери заказ вовремя',
	
	'help':
		u'Пока что я не знаю, чем тебе помочь, поэтому просто выпей кофе!'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
	db_users.check_and_add_user(message)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row('Сделать заказ')
	bot.send_message(message.from_user.id, text_messages['start'].format(name=message.from_user.first_name), reply_markup=markup)
	db_users.set_state(message.from_user.id, config.S_GET_CAT)


@bot.message_handler(commands=['help'])
def send_help(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row('Назад')
	msg = bot.send_message(message.from_user.id, text_messages['help'], reply_markup=markup)
	bot.register_next_step_handler(msg, send_welcome)