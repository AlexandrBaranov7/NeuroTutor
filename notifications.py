import pandas as pd
import menu

def make_notification(bot, message):
    bot.send_message(message.chat.id,
                     text=f'Создайте уведомление.\nНапишите текст и время уведомление в формате\n/notification <текст>::<ГГГГ-ММ-ДД ЧЧ:мм>', 
                     reply_markup=menu.return_to_main_menu_render())

def get_existing_notifications(message):
    user_id = message.from_user.id
    df = pd.read_csv('existing_notification.csv')
    textes = df[df['created_by']==user_id]['text'].tolist()
    dts = df[df['created_by']==user_id]['dt'].tolist()
    
    textes = list(map(lambda x: x[:13], textes))
    answer = [textes[i]+'... | '+dts[i] for i in range(len(textes))]
    answer_str = ''
    
    for i in answer:
        answer_str += '🔴'
        answer_str += i
        answer_str+= '\n'
    return 'Ваши уведомления:\n'+answer_str