import telebot
from telebot import types
from gh_menu import gh_menu
import db_users
from config import create_menu, Goods
import config

bot = telebot.TeleBot(config.TOKEN)

text_messages = {
	'start':
		u'Привіт, {name}!\n'
		u'Я допоможу тобі зробити онлайн замовлення (це швидко і без черги).\n\n'
		u'1. Вибери напій/десерт який тобі сподобався (Ти можеш вибрати декілька)\n'
		u'2. Оплати замовлення',
	
	'help':
		u'Поки я не знаю, чим тобі допомогти, тому просто випий каву!'
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


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_CAT)
def get_categories(message):
	user_id = message.from_user.id
	mass = list(gh_menu.keys())
	markup = create_menu(mass, back=False)
	bot.send_message(user_id, 'Что вас интересует?', reply_markup=markup)
	db_users.set_state(user_id, config.S_CHOOSE_CAT)




@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_CHOOSE_CAT)
def choose_categories(message):
	user_id = message.from_user.id

	if message.text == 'Особые напитки':
		db_users.set_state(user_id, config.S_SPECIAL_DRINKS)
		get_special_drinks(message)
	elif message.text == 'Кофе':
		db_users.set_state(user_id, config.S_COFFEE)
		get_coffee(message)
	elif message.text == 'Горячие напитки':
		db_users.set_state(user_id, config.S_HOT_DRINKS)
		get_hot_drinks(message)