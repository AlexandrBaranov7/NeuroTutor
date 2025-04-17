# Сообщения от бота. Суффикс _msg
rating_msg = 'Рейтинг БРС за выбранный период:'
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
default_error_msg = "Произошла ошибка, попробуйте позднее"
dormitory_label_msg = "Общежитие"
operational_label_msg = "Операционные платежи"
header_brs_msg = "Ваши баллы за выбранный период:\n\n"
header_no_brs_msg = "Отсутствуют баллы за выбранный период"
header_debts_msg = "Ваши долги:\n"
header_no_discipline_msg = "Нет дисциплин"
header_agreement_msg = 'Договор'
header_no_debts_msg = 'нет долгов'
unknown_msg = 'неизвестен'


# форматируемые шаблоны _template_msg
notif_created_template_msg = 'Вы успешно создали уведомление!\n\nВаше уведомление:\n\n{notif_text}\nОно будет отправлено {notif_date}.'
notif_sended_template_msg = 'Ваше уведомдение ({notif_txt}...) успешно отправлено {tg_ids_shape} cтудентам.'
instance_answer_template_msg = 'Раздел {instance}:'
debt_line_template_msg = "  Договор {contract}, долг {amount} руб"
your_disciplines_template_msg = 'Ваши дисциплины за {sem}-й семестр:\n\n'