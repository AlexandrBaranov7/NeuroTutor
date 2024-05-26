# Здесь реализованы все меню в которых может находиться пользователь, за исключением авторизации
# Авторизация реализована в authorization.py
from telebot import types 


def stunent_main_menu_render() -> types.ReplyKeyboardMarkup:
    '''
    Информирует пользователя о возвращении в главное меню
    Добавляет кнопки навигации 
    возвращает экземляр класса markup
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    docs_btn = types.KeyboardButton("📓 Документы")
    basic_info_btn = types.KeyboardButton("📝 Основная информация")
    military_btn = types.KeyboardButton("💂‍ Воинский учёт")
    financial_questions_btn = types.KeyboardButton("💸 Оплата обучения")
    quit_btn = types.KeyboardButton("❌ Выйти из своего аккаунта")

    markup.add(docs_btn,
               basic_info_btn,
               military_btn,
               financial_questions_btn,
               quit_btn)
    return markup

def return_to_main_menu_render() -> types.ReplyKeyboardMarkup:
    '''
    Возвращает markup с кнопкой возвращения в главное меню
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_return_btn = types.KeyboardButton("Вернуться в главное меню")
    markup.add(main_menu_return_btn)
    return markup

def admin_menu_render() -> types.ReplyKeyboardMarkup:
    '''
    Возвращает интерфейс администратора
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    notification_btn = types.KeyboardButton("⌛️ Прислать уведомление")
    my_notifications_btn = types.KeyboardButton("📖 Мои уведомления")
    quit_btn = types.KeyboardButton("❌ Выйти из своего аккаунта")
    markup.add(notification_btn,
               my_notifications_btn,
               quit_btn)
    return markup

def main_menu_render(role):
    if role == 'admin':
        return admin_menu_render()
    elif role == 'student':
        return stunent_main_menu_render()
        
    