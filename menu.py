# Здесь реализованы все меню в которых может находиться пользователь, за исключением авторизации
# Авторизация реализована в authorization.py
from telebot import types 


def main_menu_render() -> types.ReplyKeyboardMarkup:
    '''
    Информирует пользователя о возвращении в главное меню
    Добавляет кнопки навигации 
    возвращает экземляр класса markup
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    current_attestation_btn = types.KeyboardButton("📓 Текущая аттестация")
    inter_attestation_btn = types.KeyboardButton("📝 Промежуточная аттестация")
    study_process_btn = types.KeyboardButton("🏫 Процесс обучения")
    financial_questions_btn = types.KeyboardButton("💸 Оплата обучения")
    quit_btn = types.KeyboardButton("❌ Выйти из своего аккаунта")

    markup.add(current_attestation_btn,
               inter_attestation_btn,
               study_process_btn,
               financial_questions_btn,
               quit_btn)
    return markup

def return_to_main_menu_render():
    '''
    Возвращает markup с кнопкой возвращения в главное меню
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_return_btn = types.KeyboardButton("Вернуться в главное меню")
    markup.add(main_menu_return_btn)
    return markup