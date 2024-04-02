# Сессия авторизации реализована здесь
from telebot import types 
import pandas as pd


def request(message, bot):
    '''
    Запрос на авторизацию
    '''
    bot.send_message(message.chat.id,
                     text=f'Пожалуйста, авторизуйтесь. Для этого введите: \n/login <логин> <пароль>',
                     reply_markup=types.ReplyKeyboardRemove())
  
def validation(login, password, tg_user_id):
    '''
    Здесь ходим в базу и смотрим на наличие такого пользователя.
    Если он есть - добавляем в список авторизованных, запоминая 
    его id в базе
    '''
    active_users = pd.read_csv('active_users.csv', index_col=None)
    if login == 'admin' and password == 'admin':
        urfu_user_id = 1
        
        active_users = pd.concat([active_users,
                                  pd.DataFrame({'tg_user_id':[tg_user_id],
                                                'urfu_user_id':[urfu_user_id],
                                                'authorized':[True]})], 
                                 ignore_index=True)
        
        active_users.to_csv('active_users.csv', index=None)
        return True 
    return False

def is_authorised(tg_user_id) -> bool:
    '''
    При каждой обработке сообщения проверяем, является ли юзер
    авторизованным
    '''
    active_users = pd.read_csv('active_users.csv', index_col=None)
    cond = active_users[active_users['tg_user_id']==tg_user_id]['authorized'].values.tolist()
    if cond:
        return bool(cond[0])
    return False
    

def unlogin(tg_user_id) -> None:
    '''
    Если пользователь вышел, удаляем его из таблицы
    '''
    active_users = pd.read_csv('active_users.csv', index_col=None)
    active_users = active_users[active_users['tg_user_id']!=tg_user_id]
    active_users.to_csv('active_users.csv', index=None)
    
    