import telebot
from telebot import types
from Parser import News, Sitv

bot = telebot.TeleBot('')

@bot.message_handler(commands= ['start'])
def start(message):
    all_news = {}
    sitv = Sitv(True)
    all_news = sitv.get_news()
    bot.send_message(message.from_user.id, 'Последние новости : ')
    # for k, v in all_news.items():
    #     bot.send_message(chat_id:=message.from_user.id, text=v.get_article(), parse_mode='html')
    #     break
    bot.send_message(message.from_user.id, "<a href = ""www.ixbt.com"">www.ixbt.com</a>", parse_mode='html')

@bot.callback_query_handler (func = lambda call: True)
def logic_techsupp (call):
    if call.data == 'Да':
        bot.send_message(call.message.from_user.id, "Есть у меня немного")


"""
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    btnYes = types.KeyboardButton('Да')
    btnNo = types.KeyboardButton('Нет')
    markup.add(btnYes, btnNo)
    bot.send_message(message.from_user.id, "Привет, хочешь узнать свежие новости?", reply_markup=markup)
"""


"""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")



name = '';
surname = '';
age = 0;
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.send_message(message.from_user.id, 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?')

"""

bot.polling(none_stop=True, interval=0)
