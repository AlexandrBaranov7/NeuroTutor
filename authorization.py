# Процесс авторизации реализован здесь
from utils.inline_buttons import *
from telebot import types 
import pandas as pd
from utils.messages.from_bot_messages import *
from utils.messages.to_bot_messages import *
from DBClient import DBClient as DB
from UrfuApiClient import UrfuApiClient

db = DB('users')
api = UrfuApiClient()

def request(message, bot):
    '''
    Запрос на авторизацию
    '''
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    markup_inline.add(i_am_student_inline_button)
    markup_inline.add(i_am_admin_inline_button)
    
    bot.send_message(message.chat.id,
                     text=role_choose_msg,
                     reply_markup=markup_inline)
  
def student_login_request(message, bot):
    bot.send_message(message.chat.id,
                     text=auth_request_msg_student,
                     reply_markup=types.ReplyKeyboardRemove())

def admin_login_request(message, bot):
    bot.send_message(message.chat.id,
                     text=auth_request_msg_admin,
                     reply_markup=types.ReplyKeyboardRemove())

def validation(login, password, tg_user_id):
    '''
    Здесь ходим в базу и смотрим на наличие админа.
    Если он есть - добавляем в список авторизованных, запоминая 
    его id в базе
    '''
    role = 'unauthorized'

    if login == 'admin' and password == 'admin': # admin case
        urfu_user_id = 1
        role = 'admin'
        db.save_user(tg_id=tg_user_id, token=None, role=role)
        
    return role
         
def student_validation(minitoken, tg_id): 
    if full_name:=api.get_user_info(minitoken).get('fullName'):
        print(full_name)
        role = 'student'
    else:
        return 'unauthorized'
    db.save_user(tg_id=tg_id, token=minitoken, role=role)
    return role

def role(tg_user_id) -> bool:
    '''
    При каждой обработке сообщения проверяем, является ли юзер
    авторизованным
    '''
    
    role = db.get_user_role(tg_user_id)
    print('role requested:', role)
    if role:
        return role
    return 'unathorized'
    

def unlogin(tg_user_id) -> None:
    '''
    Если пользователь вышел, удаляем его из таблицы
    '''
    print('unlogin')
    db.del_from_users(tg_user_id)
    
    