from telebot import types
import telebot
#from <filename> import <function1>, <function2>


bot = telebot.TeleBot('943887463:AAG_SqWalzrWa3SmSmjrANf6oJ9QxD6-pzk');
	
name = '';
surname = '';
age = 0;



@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == "Привет": 
		bot.send_message(message.from_user.id,"Привет, введи команду /reg");
	elif message.text == '/reg':
		bot.send_message(message.from_user.id, "Как тебя зовут?");
		bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
	else:
		bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
	global name;
	name = message.text;
	bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
	bot.register_next_step_handler(message, get_surname);

def get_surname(message):
	global surname;
	surname = message.text;
	bot.send_message(message.from_user.id,'Сколько тебе лет?');
	bot.register_next_step_handler(message, get_age);

def get_age(message):
	global age;
	while age == 0: #проверяем что возраст изменился
		try:
			 age = int(message.text) #проверяем, что возраст введен корректно
		except Exception:
			 bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
	keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
	key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
	keyboard.add(key_yes); #добавляем кнопку в клавиатуру
	key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
	keyboard.add(key_no);
	question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
	bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
bot.polling(none_stop=True, interval=0)