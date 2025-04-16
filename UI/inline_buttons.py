from telebot import types 

# Авторизация

i_am_student_inline_button = types.InlineKeyboardButton(
    text='Я студент',
    callback_data='student_auth')

i_am_admin_inline_button = types.InlineKeyboardButton(
    text='Я администратор',
    callback_data='admin_auth')

# основная информация

schedule_first_inline_button = types.InlineKeyboardButton(
    text='Расписание, 1 курс',
    url='https://aspirant.urfu.ru/ru/aspirantura/raspisanie-zanjatii/1-kurs/',
    callback_data='schedule_first')
        
schedule_other_inline_button = types.InlineKeyboardButton(
    text='Расписание, 2-4 курс',
    url='https://aspirant.urfu.ru/ru/aspirantura/raspisanie-zanjatii/2-3-i-4-kurs/',
    callback_data='schedule_other')
        
brs_button = types.InlineKeyboardButton(
    text='Мои баллы',
    callback_data='BRS')
        
group_number_inline_button = types.InlineKeyboardButton(
    text='Номер группы',
    url='https://istudent.urfu.ru/student/data',
    callback_data='group_number')
        
study_plan_inline_button = types.InlineKeyboardButton(
    text='Учебный план',
    callback_data='study_plan')
        
science_inline_button = types.InlineKeyboardButton(
    text='Тема работы, научный руководитель',
    callback_data='science')

debts_inline_button = types.InlineKeyboardButton(
    text='Мои задолженности',
    callback_data='debts')

# оплата обучения

payyment_order_inline_button = types.InlineKeyboardButton(
    text='Актуальный приказ', callback_data='payment_order')

payment_debt_inline_button = types.InlineKeyboardButton(
    text='Задолженность за обучение',
    callback_data='payment_debt',
    url='https://istudent.urfu.ru/s/payments-and-arrears')

payyment_methods_inline_button = types.InlineKeyboardButton(
    text='Способы оплаты за обучение',
    callback_data='payment_methods')

# Документы

named_grants_inline_button = types.InlineKeyboardButton(
    text='Именные стипендии',
    callback_data='named_grants',
    url='https://aspirant.urfu.ru/ru/aspirantura/imennye-stipendii/')

doc_blanks_inline_button = types.InlineKeyboardButton(
    text='Бланки документов',
    callback_data='doc_blanks',
    url='https://aspirant.urfu.ru/ru/aspirantura/blanki-dokumentov/ ')

def generate_sem_buttons(semester: int):
    return types.InlineKeyboardButton(
        text=f'{semester} семестр',
        callback_data=f'select_semester {semester}')

def generate_period_buttons(period:str, year: str, sem:str):
    print(period)
    return types.InlineKeyboardButton(text=period,
       callback_data=f'select_period {year} {sem}')
