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
    Необходимо здесь реализовать авторизацию
    '''
    authorised = True
    if authorised:
        markup = menu.main_menu_render()
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    

# Блок обработки сообщений и навигации по боту
@bot.message_handler(content_types=['text'])
def func(message):
    '''
    Обработка сообщений
    '''
    bot.send_message(message.chat.id, text=str(message.from_user.id)+' прислал: '+message.text)
    
    if (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id,
                         text='Вы вернулись в главное меню',
                         reply_markup=menu.main_menu_render())
        
    elif(message.text in ["📓 Текущая аттестация", "📝 Промежуточная аттестация", "🏫 Процесс обучения", "💸 Оплата обучения"]):
        bot.send_message(message.chat.id,
                         text=f'Некоторые сведения об блоке {message.text} пользователя {message.from_user.id}',
                         reply_markup=menu.return_to_main_menu_render())

if __name__ == '__main__':
    bot.polling(none_stop=True)