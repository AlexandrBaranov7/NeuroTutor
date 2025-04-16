import pandas as pd
import menu
from utils.messages.from_bot_messages import *
from utils.messages.to_bot_messages import *
from ServiceContainer import service_instance
import utils.utils as utils

bot = service_instance.bot
db = service_instance.db

def make_notification(bot, message):
    bot.send_message(message.chat.id,
                     text=notif_create_request_msg, 
                     reply_markup=menu.return_to_main_menu_render())

def get_existing_notifications(message):
    user_id = message.from_user.id
    textes = [notif.text for notif in db.get_my_notifications(user_id)]
    dts = [str(notif.send_at_dt) for notif in db.get_my_notifications(user_id)]
    print(textes)
    textes = list(map(lambda x: x[:13], textes))
    answer = [textes[i]+'... | '+dts[i] for i in range(len(textes))]
    answer_str = ''
    
    for i in answer:
        answer_str += '🔴'
        answer_str += i
        answer_str+= '\n'
    return your_notifs_msg+answer_str

def create_notification(message):
    try:
        notif_text = message.text[14:]
        notif_text, notif_date = notif_text.split('::')
        notif_date =  utils.is_valid_datetime(notif_date)
        if notif_date < utils.get_current_min():
            assert ValueError
        assert notif_date != False
        db.create_notification(tg_id=message.from_user.id, text=notif_text, send_at_dt=notif_date)
        bot.send_message(message.chat.id,
                        text=notif_created_template_msg.format(notif_text=notif_text, notif_date=notif_date))
    except:
        bot.send_message(message.chat.id, format_error_msg)
        
def check_notifs():
    notifications = db.get_all_notifications()
    tg_ids = [user.telegram_id for user in db.get_all_students()]
    
    notifs = [n for n in notifications if n.send_at_dt == utils.get_current_min()]
    
    if len(notifs) > 0:
        for row in notifs:
            notif_txt = row.text
            creator = row.created_telegram_id
            bot.send_message(creator,
                                notif_sended_template_msg.format(notif_txt=notif_txt[:15],
                                                                tg_ids_shape=len(tg_ids)))
            for uid in tg_ids:
                bot.send_message(uid, text=notif_txt)
            row.delete().execute()
            