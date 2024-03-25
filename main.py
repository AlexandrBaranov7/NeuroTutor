import telebot
from telebot import types # для указание типов

bot = telebot.TeleBot('7000047042:AAF7Aat59UnnbTYO_trZXrI-dPh0dDGehAQ')

@bot.message_handler(commands=['start'])
def start(message):
    '''
    Хэндлер старта
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    hello_btn = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(hello_btn, btn2)
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}! Я бот для помощи аспирантам УрФУ", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    '''
    Основной хэндлер сообщений (ПЕРЕДЕЛАТЬ)
    '''
    if(message.text == "👋 Поздороваться"):
        bot.send_message(message.chat.id, text="Привет")
        
    elif(message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        name_btn = types.KeyboardButton("Как меня зовут?")
        what_i_can_btn = types.KeyboardButton("Что я могу?")
        back_btn = types.KeyboardButton("Вернуться в главное меню")
        markup.add(name_btn, what_i_can_btn, back_btn)
        
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif(message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "Владимир П.")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Много чего...")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
        
    else:
        bot.send_message(message.chat.id, text="На украину высылается 100 истребителей.")

bot.polling(none_stop=True)