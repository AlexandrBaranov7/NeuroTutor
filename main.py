# пользовательские модули
from utils.inline_buttons import * 
from utils.strings import * 
import utils.utils as utils

from telebot import types 
from numpy import True_

import authorization # модуль, в котором реализована авторизация и присвоение ролей
import notifications # модуль в котором реализованы уведомления
from dbclient import DBClient as DB, Notification

import pandas as pd
import threading
import environs
import datetime
import telebot
import menu
import time

env = environs.Env()
env.read_env('env.env')
token = env('TG_BOT_TOKEN') # токен телеграм бота, хранящийся в env.env
admin_id = env('ADMIN_ID')
bot = telebot.TeleBot(token)
db = DB('users')

# функции, считывающие документы
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
    
# функция будет вызываться при команде пользователя /login
@bot.message_handler(commands=['login'])
def user_login(message):
    #try:
    login_data = message.text.split()
    if len(login_data) == 3:
        _, login, password = message.text.split()
        role = authorization.validation(login, password, message.from_user.id)
        if role !='unauthorized':            
            bot.send_message(message.chat.id,
                            text=auth_success_msg,
                            reply_markup=menu.main_menu_render(role))
    elif len(login_data) == 2:
        print('student_auth')
        _, token = message.text.split()
        role = authorization.student_validation(minitoken=token, tg_id=message.from_user.id)
        if role !='unauthorized':            
            bot.send_message(message.chat.id,
                            text=auth_success_msg,
                            reply_markup=menu.main_menu_render(role))
    else:
        bot.send_message(message.chat.id,
                            text=auth_not_find_msg)
    #except:
    #    bot.send_message(message.chat.id,
    #                        text=format_error_msg)
    
# функция будет вызываться при команде /notification
@bot.message_handler(commands=['notification'])
def notification_command(message):
    role = authorization.role(message.from_user.id)
    if role == 'admin':
        notifications.create_notification(message)
    else:
        bot.send_message(message.chat.id,
                        text=not_enough_priveleges_msg)
        
@bot.message_handler(commands=['feedback'])
def feedback_collect(message):
    '''
    Функция для сбора отзывов
    '''
    feedback_text = message.text
    bot.send_message(admin_id, 'Новый отзыв о боте:\n'+feedback_text)
    bot.send_message(message.chat.id, 'Ваш отзыв успешно доставлен администратору!')

# блок обработки сообщений
def instance_answer(message) -> None:
    """
    Функция instance_answer, 
    Принимает:
        Объект типа message (сообщения)
    Возвращает:
        None
    """
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

        
# обработка callback, получаемых при нажатии пользователем на inline-кнопки      
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    call_data = call.data
    print(call.from_user.username, ' : callback - ', call.data)
    
    if call_data  == 'student_auth':
        authorization.student_login_request(call.message, bot)
        
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
    print(message.from_user.username, ' : ', message.text)
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
    while True:
        try: 
            bot.polling(none_stop=True, logger_level=40)
        except:
            print('Polling error, retry in 5 seconds...')
            time.sleep(5)
            
def notif_checker():
    while True:
        #try: 
        notifications.check_notifs()
        time.sleep(10)
        #except:
        #    print('Notification checking error, retry in 5 seconds...')
        #    time.sleep(5)

def main():
    polling_thread = threading.Thread(target=polling)
    notif_thread = threading.Thread(target=notif_checker)
    
    polling_thread.start()
    notif_thread.start()
    
if __name__ == '__main__':
    main()
    