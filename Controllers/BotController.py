from UI.inline_buttons import * 
from UI.inline_buttons import generate_period_buttons, generate_sem_buttons
from utils.pathes import * 
from UI.messages.from_bot_messages import *
from UI.messages.to_bot_messages import *

from telebot import types

import Controllers.AuthorizationController as AuthorizationController # модуль, в котором реализована авторизация и присвоение ролей
import Controllers.NotificationsController as NotificationsController # модуль в котором реализованы уведомления
from info_docs.FileManager import FileManager
from Services.ServiceContainer import ServiceContainer

import UI.menu as menu
import time

class BotController:
    def __init__(self, services: ServiceContainer, file_manager: FileManager):
        self.bot = services.bot
        self.db = services.db
        self.api = services.api
        self.admin_id = services.admin_id
        self.files = file_manager
        self._register_handlers()

    def _register_handlers(self):
        handlers_commands = {
            'start': self.start,
            'login': self.user_login,
            'notification': self.notification_command,
            'feedback': self.feedback_collect,
        }
        for cmd, func in handlers_commands.items():
            self.bot.message_handler(commands=[cmd])(func)

        self.bot.callback_query_handler(func=lambda call: True)(self.answer)
        self.bot.message_handler(content_types=['text'])(self.message_process)

    def start(self, message):
        self.bot.send_message(message.chat.id, welcome_msg, reply_markup=types.ReplyKeyboardRemove())
        AuthorizationController.request(message, self.bot)

    def user_login(self, message):
        login_data = message.text.split()
        try:
            if len(login_data) == 3:
                _, login, password = login_data
                role = AuthorizationController.validation(login, password, message.from_user.id)
                if role != 'unauthorized':
                    self._send_main_menu(message.chat.id, role)
            elif len(login_data) == 2:
                _, token = login_data
                role = AuthorizationController.student_validation(token, message.from_user.id)
                if role != 'unauthorized':
                    full_name = self.api.get_user_info(self.db.get_minitoken(message.chat.id)).get('fullName')
                    name = ' '.join(full_name.split()[1:])
                    self.bot.send_message(message.chat.id, f'Добро пожаловать, {name}!')
                    self._send_main_menu(message.chat.id, role)
                else:
                    self._send_auth_fail(message, role)
            else:
                self.bot.send_message(message.chat.id, auth_not_find_msg)
        except Exception as e:
            ... # must be logging

    def notification_command(self, message):
        if AuthorizationController.role(message.from_user.id) == 'admin':
            NotificationsController.create_notification(message)
        else:
            self.bot.send_message(message.chat.id, not_enough_priveleges_msg)

    def feedback_collect(self, message):
        self.bot.send_message(self.admin_id, f'Новый отзыв о боте:\n{message.text}')
        self.bot.send_message(message.chat.id, 'Ваш отзыв успешно доставлен администратору!')

    def instance_answer(self, message):
        text = message.text
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        templates = {
            payment_text: [payyment_order_inline_button, payment_debt_inline_button, payyment_methods_inline_button],
            basic_info_text: [
                schedule_first_inline_button, schedule_other_inline_button, brs_button,
                debts_inline_button, group_number_inline_button, study_plan_inline_button, science_inline_button
            ],
            docs_text: [named_grants_inline_button, doc_blanks_inline_button],
        }

        if text == military_order_text:
            self.bot.send_message(message.chat.id, actual_military_order_msg)
            self.bot.send_document(message.chat.id, self.files.military_order())
        elif text in templates:
            for btn in templates[text]:
                markup_inline.add(btn)
            msg = instance_answer_template_msg.format(instance=text)
            self.bot.send_message(message.chat.id, msg, reply_markup=markup_inline)

    def answer(self, call):
        data = call.data
        chat_id = call.message.chat.id
        tg_id = call.from_user.id

        match data:
            case 'student_auth':
                AuthorizationController.student_login_request(call.message, self.bot)
            case 'admin_auth':
                AuthorizationController.admin_login_request(call.message, self.bot)
            case 'payment_order':
                self._send_document(chat_id, actual_payment_order_msg, self.files.payment_order())
            case 'payment_methods':
                self.bot.send_message(chat_id, payment_methods_msg)
            case 'science':
                self.bot.send_document(chat_id, self.files.students_list())
            case 'study_plan':
                self._send_study_plan(chat_id, tg_id)
            case _ if data.startswith('select_semester'):
                sem = int(data.split()[-1])
                self.bot.send_message(chat_id, self.api.get_eduplan(self.db.get_minitoken(chat_id), sem))
            case 'BRS':
                self._send_periods(chat_id)
            case _ if data.startswith('select_period'):
                year, sem = data.split()[1:]
                self.bot.send_message(chat_id, self.api.get_brs(self.db.get_minitoken(chat_id), year, sem))
            case 'debts':
                self.bot.send_message(chat_id, self.api.get_debts(self.db.get_minitoken(chat_id)))

    def message_process(self, message):
        user_id = message.from_user.id
        text = message.text
        role = AuthorizationController.role(user_id)

        if role != 'unathorized':
            match text:
                case _ if text == return_main_menu_text:
                    self._send_main_menu(message.chat.id, role)
                case _ if text in [docs_text, basic_info_text, military_order_text, payment_text]:
                    self.instance_answer(message)
                case _ if text == quit_text:
                    self.bot.send_message(message.chat.id, quited_msg)
                    AuthorizationController.unlogin(user_id)
                    self.start(message)
                case _ if text == create_notif_text and role == 'admin':
                    NotificationsController.make_notification(self.bot, message)
                case _ if text == my_notifs_text and role == 'admin':
                    nots = NotificationsController.get_existing_notifications(message)
                    self.bot.send_message(message.chat.id, text=nots)
        else:
            AuthorizationController.request(message, self.bot)

    def polling(self):
        while True:
            self.bot.polling(none_stop=True, logger_level=40)

    def notif_checker(self):
        while True:
            NotificationsController.check_notifs()
            time.sleep(10)

    # Вспомогательные методы
    def _send_main_menu(self, chat_id, role):
        self.bot.send_message(chat_id, auth_success_msg, reply_markup=menu.main_menu_render(role))

    def _send_auth_fail(self, message, role):
        self.bot.send_message(message.chat.id, auth_not_find_msg, reply_markup=menu.main_menu_render(role))
        AuthorizationController.student_login_request(message, self.bot)

    def _send_document(self, chat_id, msg, file):
        self.bot.send_message(chat_id, msg)
        self.bot.send_document(chat_id, file)

    def _send_study_plan(self, chat_id, tg_id):
        semesters = self.api.get_semesters(token=self.db.get_minitoken(tg_id))
        if isinstance(semesters, list):
            markup = types.InlineKeyboardMarkup(row_width=1)
            for sem in semesters:
                markup.add(generate_sem_buttons(sem))
            self.bot.send_message(chat_id, 'Выберите семестр:', reply_markup=markup)
        else:
            self.bot.send_message(chat_id, semesters)

    def _send_periods(self, chat_id):
        periods_mapping = {'autumn': 'Осень', 'spring': 'Весна'}
        periods_data = self.api.get_periods(self.db.get_minitoken(chat_id))
        if isinstance(periods_data, str):
            self.bot.send_message(chat_id, periods_data)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for year in periods_data:
                for sem in year['semesters']:
                    period = f'{year["year"]} - {periods_mapping[sem]}'
                    btn = generate_period_buttons(period, year['year'], sem)
                    markup.add(btn)
            self.bot.send_message(chat_id, 'Выберите период:', reply_markup=markup)