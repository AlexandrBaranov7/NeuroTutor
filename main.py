from inline_buttons import *
from telebot import types 
from numpy import True_
import authorization
import notifications
import pandas as pd
import threading
import environs
import datetime
import telebot
import utils
import menu
import time

env = environs.Env()
env.read_env('env.env')
token = env('TG_BOT_TOKEN')
bot = telebot.TeleBot(token)

def payment_order(): return open(r'Приказ_о_стоимости_обучения_аспирантов_на_2024_2025_учебный_год.pdf', 'rb')
def millitary_order(): return open(r"Приказ_Об_организации_воинского_учета_граждан,_в_т_ч_бронировнаия.PDF", 'rb')
def students_list(): return open(r"Списки аспирантов.xlsx", 'rb')

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


def instance_answer(message):
    text = message.text
    answer = f'Раздел {text}:'
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    if text == "💸 Оплата обучения":

        markup_inline.add(payyment_order_inline_button)
        markup_inline.add(payment_debt_inline_button)
        markup_inline.add(payyment_methods_inline_button)
        
        
        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == "📝 Основная информация":
         
        markup_inline.add(schedule_first_inline_button)
        markup_inline.add(schedule_other_inline_button)
        markup_inline.add(session_inter_inline_button)
        markup_inline.add(session_current_inline_button)
        markup_inline.add(group_number_inline_button)
        markup_inline.add(study_plan_inline_button)
        markup_inline.add(science_inline_button)

        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == "📓 Документы":
        markup_inline.add(named_grants_inline_button)
        markup_inline.add(doc_blanks_inline_button)
        
        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == "💂‍ Воинский учёт":
        msg = 'Актуальный приказ об организации воинского учёта:'
        bot.send_message(message.chat.id, msg)
        bot.send_document(message.chat.id, millitary_order())

        
        
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    call_data = call.data
    if call_data  == 'student_auth':
        role = authorization.validation('student', 'student', call.message.chat.id)
        if role !='unauthorized':            
            bot.send_message(call.message.chat.id,
                            text=f'Вы успешно авторизовались!',
                            reply_markup=menu.main_menu_render(role))
        else:
            bot.send_message(call.message.chat.id,
                                text='Похоже, такого пользователя нет.')
    if call_data  == 'admin_auth':
        authorization.admin_login_request(call.message, bot)
    elif call.data == 'payment_order':
        msg = 'Актуальный приказ по оплате за обучение:'
        bot.send_message(call.message.chat.id, msg)
        bot.send_document(call.message.chat.id, payment_order())
        
    elif call.data == 'payment_methods':
        msg = ''' Способы оплаты за обучение\n
Оплата может быть произведена следующими способами:
1.	Через личный кабинет аспиранта (раздел документы и финансы => Финансовые сервисы => Информация о состоянии расчетов по платным образовательным услугам)\n
2.	Через банк (при себе необходимо иметь дополнительное соглашение, которое было выдано Вам в начале учебного года)\n
3.	Через QR-код на договоре об оплате'''
        bot.send_message(call.message.chat.id, msg)
        
    elif call_data == 'science':
        bot.send_document(call.message.chat.id, students_list())

        

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
        
        elif(message.text in ["📓 Документы", "📝 Основная информация", "💂‍ Воинский учёт", "💸 Оплата обучения"]):
            instance_answer(message)

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
    