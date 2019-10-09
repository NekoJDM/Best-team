from telebot import types

import db_users
from gh_menu import gh_menu

TOKEN = '943887463:AAG_SqWalzrWa3SmSmjrANf6oJ9QxD6-pzk'


# КОНСТАНТЫ СОСТОЯНИЙ
S_GET_CAT = 'Список категорий'
S_CHOOSE_CAT = 'Выбор категории'

# КОНСТАНТЫ КАТЕГОРИЙ
S_SPECIAL_DRINKS = 'Особые напитки'
S_COFFEE = 'Кофе'
S_HOT_DRINKS = 'Горячие напитки'

# КОНСТАНТЫ ТОВАРОВ
S_CHOOSE_GOOD = 'Выбор товара'

S_LATTE_LAVANDA_SHALFEI = 'Латте Лаванда Шалфей'
S_RAF_LEMON_PIE = 'Раф Лимонный Пай'


S_KAPUCHINO = 'Капучино'
S_LATTE_MAKIATO = 'Латте Макиато'


S_KAKAO = 'Какао'
S_TEA = 'Чай'





#ОСОБЫЕ НАПИТКИ
#list_of_latte = ['Латте Лаванда Шалфей']




def create_menu(mass, back=True):
	"""
	This function allows to creat menu of buttons.
	mass - the list of string
	back - back button, if true, add a button back. Default back=True
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	if len(mass) == 1:
		markup.row(mass[0])
	else:
		while len(mass) > 0:
			try:
				cut = mass[:2]
				markup.row(cut[0], cut[1])
				del mass[:2]
				
				if len(mass) == 1:
					markup.row(mass[0])
					break
			except:
				print('WTF')
	

	if back == True:
		markup.row('Назад')
	
	return markup
def create_menu1(mass, back=True):
	"""
	This function allows to creat menu of buttons.
	mass - the list of string
	back - back button, if true, add a button back. Default back=True
	"""
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	if len(mass) == 1:
		markup.row(mass[0])
	else:
		while len(mass) > 0:
			try:
				cut = mass[:2]
				markup.row(cut[0], cut[1])
				del mass[:2]
				
				if len(mass) == 1:
					markup.row(mass[0])
					break
			except:
				print('WTF')
	

	if back == True:
		markup.row('Назадд')
	
	return markup

class Goods:
	def __init__(self, bot, message, state):
		self.bot = bot
		self.message = message
		self.state = state

	def get_goods_list(self):
		"""
		This function allows to get a list of special drinks
		"""
		user_id = self.message.from_user.id
		mass = list(gh_menu[self.message.text])
		print(mass)
		markup = create_menu(mass)
		self.bot.send_message(user_id, 'Выберите напиток', reply_markup=markup)
		db_users.set_state(user_id, self.state)

	def get_current_good(self, cat):
		"""
		This function allows to get a current good
		"""
		user_id = self.message.from_user.id
		mass = list(gh_menu[cat][self.message.text])
		markup = create_menu(mass)
		self.bot.send_message(user_id, 'Выберите размер', reply_markup=markup)
		db_users.set_state(user_id, self.state)
