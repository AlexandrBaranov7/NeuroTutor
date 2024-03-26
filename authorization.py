# Сессия авторизации реализована здесь
from telebot import types 


def request(message, bot):
    bot.send_message(message.chat.id,
                     text=f'Добро пожаловать!\n\nПожалуйста, авторизуйтесь. Для этого введите: \n/login <логин> <пароль>',
                     reply_markup=types.ReplyKeyboardRemove())
  
def validation(login, password):
    if login == 'admin' and password == 'admin':
        return True 
    return False

def is_authorised(tg_user_id):
    return True

