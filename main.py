import telebot
import environs
from telebot import types 
import menu
import authorization

env = environs.Env()
env.read_env('env.env')
token = env('TG_BOT_TOKEN')

bot = telebot.TeleBot(token)

# Блок авторизации
@bot.message_handler(commands=['start'])
def start(message):
    '''
    Первоначально необходимо запросить авторизацию
    '''
    authorization.request(message, bot)
    
@bot.message_handler(commands=['login'])
def login(message):
    try:
        _, login, password = message.text.split()
        if authorization.validation(login, password):
            bot.send_message(message.chat.id,
                            text=f'Вы успешно авторизовались!',
                            reply_markup=menu.main_menu_render())
        else:
            bot.send_message(message.chat.id,
                             text='Похоже, такого пользователя нет.')
    except:
        bot.send_message(message.chat.id,
                            text=f'Проверьте формат вводимых данных')
    

# Блок обработки сообщений и навигации по боту
@bot.message_handler(content_types=['text'])
def func(message):
    '''
    Обработка сообщений
    '''
    if authorization.is_authorised(message.from_user.id):
        bot.send_message(message.chat.id, text=str(message.from_user.id)+' прислал: '+message.text)
    
        if (message.text == "Вернуться в главное меню"):
            bot.send_message(message.chat.id,
                             text='Вы вернулись в главное меню',
                             reply_markup=menu.main_menu_render())
        
        elif(message.text in ["📓 Текущая аттестация", "📝 Промежуточная аттестация", "🏫 Процесс обучения", "💸 Оплата обучения"]):
            bot.send_message(message.chat.id,
                             text=f'Некоторые сведения об блоке {message.text} пользователя {message.from_user.id}',
                             reply_markup=menu.return_to_main_menu_render())
        elif(message.text == "❌ Выйти из своего аккаунта"):
            bot.send_message(message.chat.id,
                             text=f'Вы вышли из своего аккаунта')
            start(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)