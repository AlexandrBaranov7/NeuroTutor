from numpy import True_
import telebot
import environs
from telebot import types 
import menu
import authorization
import notifications
import pandas as pd
import threading
import datetime
import utils
import time

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
    bot.send_message(message.chat.id,
                     text=f'Добро пожаловать!',
                     reply_markup=types.ReplyKeyboardRemove())
    authorization.request(message, bot)
    
@bot.message_handler(commands=['login'])
def user_login(message):
    try:
        _, login, password = message.text.split()
        role = authorization.validation(login, password, message.from_user.id)
        if role !='unauthorized':            
            bot.send_message(message.chat.id,
                            text=f'Вы успешно авторизовались!',
                            reply_markup=menu.main_menu_render(role))
        else:
            bot.send_message(message.chat.id,
                                text='Похоже, такого пользователя нет.')
    except:
        bot.send_message(message.chat.id,
                            text=f'Проверьте формат вводимых данных')
    
@bot.message_handler(commands=['notification'])
def notification_command(message):
    role = authorization.role(message.from_user.id)
    if role == 'admin':
        notif_text = message.text[14:]
        try:
            notif_text, notif_date = notif_text.split('::')
            notif_date =  utils.is_valid_datetime(notif_date)
            if notif_date < utils.get_current_min():
                assert ValueError
            assert notif_date != False
            notifications_df = pd.read_csv('existing_notification.csv', index_col=None)
        
            notifications_df = pd.concat([notifications_df,
                                         pd.DataFrame({'created_by':[message.from_user.id],
                                                       'text':[notif_text],
                                                       'dt':[notif_date]})])
        
            notifications_df.to_csv('existing_notification.csv', index=None)
            bot.send_message(message.chat.id,
                            text=f'Вы успешно создали уведомление!\n\nВаше уведомление:\n\n{notif_text}\nОно будет отправлено {notif_date}.')
        except:
            bot.send_message(message.chat.id, 'Проверьте формат вводимых данных')
    else:
        bot.send_message(message.chat.id,
                        text=f'Недостаточно прав для создания уведомления')

# Блок обработки сообщений и навигации по боту
@bot.message_handler(content_types=['text'])
def func(message):
    '''
    Обработка сообщений
    '''
    if authorization.role(message.from_user.id) != 'unathorized':
        role = authorization.role(message.from_user.id)
        if (message.text == "Вернуться в главное меню"):
            bot.send_message(message.chat.id,
                             text='Вы вернулись в главное меню',
                             reply_markup=menu.main_menu_render(role))
        
        elif(message.text in ["📓 Текущая аттестация", "📝 Промежуточная аттестация", "🏫 Процесс обучения", "💸 Оплата обучения"]):
            bot.send_message(message.chat.id,
                             text=f'Некоторые сведения об блоке {message.text} пользователя {message.from_user.id}',
                             reply_markup=menu.return_to_main_menu_render())
        elif(message.text == "❌ Выйти из своего аккаунта"):
            bot.send_message(message.chat.id,
                             text=f'Вы вышли из своего аккаунта')
            authorization.unlogin(message.from_user.id)
            start(message)
        # admin actions
        elif(message.text == "⌛️ Прислать уведомление") and role == 'admin':
            notifications.make_notification(bot, message)
        elif(message.text == "📖 Мои уведомления") and role == 'admin':
            nots = notifications.get_existing_notifications(message)
            bot.send_message(message.chat.id, text=nots)
    else:
         authorization.request(message, bot)

def polling():
    bot.polling(none_stop=True, logger_level=40)
    
def notif_checker():
    while True:
        notifications_df = pd.read_csv('existing_notification.csv', index_col=None)
        users = pd.read_csv('active_users.csv', index_col=None)
        
        tg_ids = users[users['role']=='student']['tg_user_id']
        
        notifs = notifications_df[notifications_df['dt'].astype(str)==str(utils.get_current_min())]
        if notifs.shape[0] != 0:
            for index, row in notifs.iterrows():
                notif_txt = row['text']
                creator = row['created_by']
                bot.send_message(creator, f'Ваше уведомдение ({notif_txt[:15]}...) успешно отправлено {tg_ids.shape[0]} cтудентам.')
                for uid in tg_ids:
                    bot.send_message(uid, text=notif_txt)
            notifications_df = notifications_df[notifications_df['dt'].astype(str)!=str(utils.get_current_min())]

        notifications_df = notifications_df[notifications_df['dt'].astype(str)>=str(utils.get_current_min())]
        notifications_df.to_csv('existing_notification.csv', index=None)
        time.sleep(20)

def main():
    polling_thread = threading.Thread(target=polling)
    notif_thread = threading.Thread(target=notif_checker)
    
    polling_thread.start()
    notif_thread.start()
    
if __name__ == '__main__':
    main()
    