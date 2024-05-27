# Процесс авторизации реализован здесь
from inline_buttons import *
from telebot import types 
import pandas as pd
from strings import *

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
  
def admin_login_request(message, bot):
    bot.send_message(message.chat.id,
                     text=auth_request_msg,
                     reply_markup=types.ReplyKeyboardRemove())

def validation(login, password, tg_user_id):
    '''
    Здесь ходим в базу и смотрим на наличие такого пользователя.
    Если он есть - добавляем в список авторизованных, запоминая 
    его id в базе
    '''
    active_users = pd.read_csv(active_users_path, index_col=None)
    role = 'unauthorized'

    if login == 'admin' and password == 'admin': # admin case
        urfu_user_id = 1
        role = 'admin'
        
        active_users = pd.concat([active_users,
                                  pd.DataFrame({'tg_user_id':[tg_user_id],
                                                'urfu_user_id':[urfu_user_id],
                                                'authorized':[True],
                                                'role':[role]})], 
                                 ignore_index=True)
        active_users = active_users.drop_duplicates(subset='tg_user_id', keep='last')
        
        active_users.to_csv(active_users_path, index=None)
         
        
    elif login == 'student' and password == 'student': # student case
        urfu_user_id = 2
        role = 'student'

        active_users = pd.concat([active_users,
                                  pd.DataFrame({'tg_user_id':[tg_user_id],
                                                'urfu_user_id':[urfu_user_id],
                                                'authorized':[True],
                                                'role':[role]})], 
                                 ignore_index=True)
        active_users = active_users.drop_duplicates(subset='tg_user_id', keep='last')
        
        active_users.to_csv(active_users_path, index=None)
          
    return role

def role(tg_user_id) -> bool:
    '''
    При каждой обработке сообщения проверяем, является ли юзер
    авторизованным
    '''
    active_users = pd.read_csv(active_users_path, index_col=None)
    role = active_users[active_users['tg_user_id']==tg_user_id]['role'].values.tolist()
    if len(role):
        return role[0]
    return 'unathorized'
    

def unlogin(tg_user_id) -> None:
    '''
    Если пользователь вышел, удаляем его из таблицы
    '''
    active_users = pd.read_csv(active_users_path, index_col=None)
    active_users = active_users[active_users['tg_user_id']!=tg_user_id]
    active_users.to_csv(active_users_path, index=None)
    
    