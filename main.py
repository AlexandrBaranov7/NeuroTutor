from inline_buttons import *
from telebot import types 
from numpy import True_
from strings import *
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

def payment_order(): return open(costs_order_path, 'rb')
def millitary_order(): return open(military_order_path, 'rb')
def students_list(): return open(students_list_path, 'rb')

# Блок авторизации
@bot.message_handler(commands=['start'])
def start(message):
    '''
    Первоначально необходимо запросить авторизацию
    '''
    
    bot.send_message(message.chat.id,
                     text=welcome_msg,
                     reply_markup=types.ReplyKeyboardRemove())

    authorization.request(message, bot)
    
@bot.message_handler(commands=['login'])
def user_login(message):
    try:
        _, login, password = message.text.split()
        role = authorization.validation(login, password, message.from_user.id)
        if role !='unauthorized':            
            bot.send_message(message.chat.id,
                            text=auth_success_msg,
                            reply_markup=menu.main_menu_render(role))
        else:
            bot.send_message(message.chat.id,
                                text=auth_not_find_msg)
    except:
        bot.send_message(message.chat.id,
                            text=format_error_msg)
    
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
            notifications_df = pd.read_csv(existing_notification_path, index_col=None)
        
            notifications_df = pd.concat([notifications_df,
                                         pd.DataFrame({'created_by':[message.from_user.id],
                                                       'text':[notif_text],
                                                       'dt':[notif_date]})])
        
            notifications_df.to_csv(existing_notification_path, index=None)
            bot.send_message(message.chat.id,
                            text=notif_created_template_msg.format(notif_text=notif_text, notif_date=notif_date))
        except:
            bot.send_message(message.chat.id, format_error_msg)
    else:
        bot.send_message(message.chat.id,
                        text=not_enough_priveleges_msg)


def instance_answer(message):
    text = message.text
    answer = instance_answer_template_msg.format(instance=text)
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    if text == payment_text:

        markup_inline.add(payyment_order_inline_button)
        markup_inline.add(payment_debt_inline_button)
        markup_inline.add(payyment_methods_inline_button)
        
        
        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == basic_info_text:
         
        markup_inline.add(schedule_first_inline_button)
        markup_inline.add(schedule_other_inline_button)
        markup_inline.add(session_inter_inline_button)
        markup_inline.add(session_current_inline_button)
        markup_inline.add(group_number_inline_button)
        markup_inline.add(study_plan_inline_button)
        markup_inline.add(science_inline_button)

        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == docs_text:
        markup_inline.add(named_grants_inline_button)
        markup_inline.add(doc_blanks_inline_button)
        
        bot.send_message(message.chat.id, answer,
                            reply_markup=markup_inline)
        
    elif text == military_order_text:
        msg = actual_military_order_msg
        bot.send_message(message.chat.id, msg)
        bot.send_document(message.chat.id, millitary_order())

        
        
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    call_data = call.data
    if call_data  == 'student_auth':
        role = authorization.validation('student', 'student', call.message.chat.id)
        if role !='unauthorized':            
            bot.send_message(call.message.chat.id,
                            text=auth_success_msg,
                            reply_markup=menu.main_menu_render(role))
        else:
            bot.send_message(call.message.chat.id,
                                text=auth_not_find_msg)
    if call_data  == 'admin_auth':
        authorization.admin_login_request(call.message, bot)
    elif call.data == 'payment_order':
        msg = actual_payment_order_msg
        bot.send_message(call.message.chat.id, msg)
        bot.send_document(call.message.chat.id, payment_order())
        
    elif call.data == 'payment_methods':
        msg = payment_methods_msg
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
        if (message.text == return_main_menu_text):
            bot.send_message(message.chat.id,
                             text=returned_to_main_menu_msg,
                             reply_markup=menu.main_menu_render(role))
        
        elif(message.text in [docs_text, basic_info_text, military_order_text, payment_text]):
            instance_answer(message)

        elif(message.text == quit_text):
            bot.send_message(message.chat.id,
                             text=quited_msg)
            authorization.unlogin(message.from_user.id)
            start(message)
            
        # admin actions
        elif(message.text == create_notif_text) and role == 'admin':
            notifications.make_notification(bot, message)
        elif(message.text == my_notifs_text) and role == 'admin':
            nots = notifications.get_existing_notifications(message)
            bot.send_message(message.chat.id, text=nots)
    else:
         authorization.request(message, bot)

def polling():
    bot.polling(none_stop=True, logger_level=40)
    
def notif_checker():
    while True:
        notifications_df = pd.read_csv('existing_notification.csv', index_col=None)
        users = pd.read_csv(active_users_path, index_col=None)
        
        tg_ids = users[users['role']=='student']['tg_user_id']
        
        notifs = notifications_df[notifications_df['dt'].astype(str)==str(utils.get_current_min())]
        if notifs.shape[0] != 0:
            for index, row in notifs.iterrows():
                notif_txt = row['text']
                creator = row['created_by']
                bot.send_message(creator, notif_created_template_msg.format(notif_text=notif_txt[:15], tg_ids_shape=tg_ids.shape[0]))
                for uid in tg_ids:
                    bot.send_message(uid, text=notif_txt)
            notifications_df = notifications_df[notifications_df['dt'].astype(str)!=str(utils.get_current_min())]

        notifications_df = notifications_df[notifications_df['dt'].astype(str)>=str(utils.get_current_min())]
        notifications_df.to_csv(existing_notification_path, index=None)
        time.sleep(20)

def main():
    polling_thread = threading.Thread(target=polling)
    notif_thread = threading.Thread(target=notif_checker)
    
    polling_thread.start()
    notif_thread.start()
    
if __name__ == '__main__':
    main()
    