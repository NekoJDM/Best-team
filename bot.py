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



@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_SPECIAL_DRINKS)
def get_special_drinks(message):

	special_drinks = Goods(bot, message, config.S_CHOOSE_GOOD)
	special_drinks.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_COFFEE)
def get_coffee(message):

	coffee = Goods(bot, message, config.S_CHOOSE_GOOD)
	coffee.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_HOT_DRINKS)
def get_hot_drinks(message):

	hot_drinks = Goods(bot, message, config.S_CHOOSE_GOOD)
	hot_drinks.get_goods_list()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_CHOOSE_GOOD)
def choose_good(message):

	user_id = message.from_user.id
	if message.text == "Назад":
		db_users.set_state(user_id, config.S_CHOOSE_CAT)
		get_categories(message)
	if message.text == 'Латте Лаванда Шалфей':
		db_users.set_state(user_id, config.S_LATTE_LAVANDA_SHALFEI)
		get_latte_lavanda_shalfei(message)
	elif message.text == 'Раф Лимонный Пай':
		db_users.set_state(user_id, config.S_RAF_LEMON_PIE)
		get_raf_lemon_pie(message)
	elif message.text == 'Капучино':
		db_users.set_state(user_id, config.S_KAPUCHINO)
		get_kapuchino(message)
	elif message.text == 'Латте Макиато':
		db_users.set_state(user_id, config.S_LATTE_MAKIATO)
		get_latte_makiato(message)
	elif message.text == 'Какао':
		db_users.set_state(user_id, config.S_KAKAO)
		get_kakao(message)
	elif message.text == 'Чай':
		db_users.set_state(user_id, config.S_TEA)
		get_tea(message)

# Функція Пилипчука
@bot.message_handler(func=lambda message: (db_users.get_current_state(message.from_user.id) == config.S_LATTE_LAVANDA_SHALFEI) or (db_users.get_current_state(message.from_user.id) == config.S_RAF_LEMON_PIE) )
def choose_good1(message):

	user_id = message.from_user.id
	if message.text == "Назад":
		db_users.set_state(user_id, config.S_SPECIAL_DRINKS)
		message.text = 'Особые напитки'
		get_special_drinks(message)

# Функція Поліщука
@bot.message_handler(func=lambda message: (db_users.get_current_state(message.from_user.id) == config.S_KAPUCHINO) or (db_users.get_current_state(message.from_user.id) == config.S_LATTE_MAKIATO) )
def choose_good2(message):
	user_id = message.from_user.id
	if message.text == "Назад":
		db_users.set_state(user_id, config.S_COFFEE)
		message.text = 'Кофе'
		get_special_drinks(message)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_LATTE_LAVANDA_SHALFEI)
def get_latte_lavanda_shalfei(message):

	latte_lavanda_shalfei = Goods(bot, message, config.S_LATTE_LAVANDA_SHALFEI)
	latte_lavanda_shalfei.get_current_good(config.S_SPECIAL_DRINKS)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_RAF_LEMON_PIE)
def get_raf_lemon_pie(message):

	raf_lemon_pie = Goods(bot, message, config.S_RAF_LEMON_PIE)
	raf_lemon_pie.get_current_good(config.S_SPECIAL_DRINKS)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_KAPUCHINO)
def get_kapuchino(message):

	kapuchino = Goods(bot, message, config.S_KAPUCHINO)
	kapuchino.get_current_good(config.S_COFFEE)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_LATTE_MAKIATO)
def get_latte_makiato(message):

	latte_makiato = Goods(bot, message, config.S_LATTE_MAKIATO)
	latte_makiato.get_current_good(config.S_COFFEE)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_KAKAO)
def get_kakao(message):

	kakao = Goods(bot, message, config.S_KAKAO)
	kakao.get_current_good(config.S_HOT_DRINKS)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_TEA)
def get_tea(message):

	tea = Goods(bot, message, config.S_TEA)
	tea.get_current_good(config.S_HOT_DRINKS)



bot.polling(none_stop=True)