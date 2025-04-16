# тут будут лежать всякие строки, для удобства обращения к ним в коде


# Пути. Суффикс _path
costs_order_path = r'info_docs/Приказ_о_стоимости_обучения_аспирантов_на_2024_2025_учебный_год.pdf'
military_order_path = r'info_docs/Приказ_Об_организации_воинского_учета_граждан,_в_т_ч_бронировнаия.PDF'
students_list_path = r'info_docs/Списки аспирантов.xlsx'
existing_notification_path = r'backend_data/existing_notification.csv'
active_users_path = r'backend_data/active_users.csv'
    
# Сообщения от бота. Суффикс _msg
welcome_msg = 'Приветствуем вас в «Нейротьюторе» — умном боте, который поможет аспирантам в обучении!'
auth_success_msg = 'Вход выполнен успешно!'
auth_not_find_msg = 'Похоже, что такого пользователя не существует.'
format_error_msg = 'Пожалуйста, проверьте, правильно ли вы ввели данные.'
not_enough_priveleges_msg = 'У вас недостаточно прав для отправки уведомления.'
actual_military_order_msg = 'Актуальный приказ об организации воинского учёта:'
actual_payment_order_msg = 'Актуальный приказ по оплате за обучение:'
returned_to_main_menu_msg = 'Вы вернулись на главную страницу.'
quited_msg = 'Вы вышли из своего аккаунта'
role_choose_msg = 'Пожалуйста, выберите роль:'
auth_request_msg_admin = 'Пожалуйста, авторизуйтесь. Для этого введите:\n/login <логин> <пароль>'
auth_request_msg_student = '''Пожалуйста, авторизуйтесь. Для этого введите:
/login <ваш токен>.

Ссылка для получения токена: https://minitoken-test.my1.urfu.ru 

Авторизуйтесь в домене @at.urfu.ru'''
notif_create_request_msg = 'Создайте уведомление.\nУкажите текст и время уведомления в формате\n/notification <текст>::<ГГГГ-ММ-ДД ЧЧ:мм>'
your_notifs_msg = 'Ваши уведомления:\n'
payment_methods_msg = ''' Способы оплаты за обучение:

1. Через личный кабинет аспиранта: раздел «Документы и финансы» — «Финансовые сервисы» — «Информация о состоянии расчётов по платным образовательным услугам».

2. Через банк, имея при себе дополнительное соглашение, выданное в начале учебного года.

3. Через QR-код на договоре об оплате.'''
    
# Запросы к боту. Суффикс _text
payment_text = "💸 Оплата обучения"
basic_info_text = "📝 Основная информация"
docs_text = "📓 Документы"
military_order_text = "💂‍ Воинский учёт"
return_main_menu_text = "Вернуться в главное меню"
quit_text = "❌ Выйти из своего аккаунта"
create_notif_text = "⌛️ Прислать уведомление"
my_notifs_text = "📖 Мои уведомления"
    
# форматируемые шаблоны
notif_created_template_msg = 'Вы успешно создали уведомление!\n\nВаше уведомление:\n\n{notif_text}\nОно будет отправлено {notif_date}.'
notif_sended_template_msg = 'Ваше уведомдение ({notif_txt}...) успешно отправлено {tg_ids_shape} cтудентам.'
instance_answer_template_msg = 'Раздел {instance}:'