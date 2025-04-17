import peewee as pw
from typing import Union

db_source = "backend_data/users.db"

class User(pw.Model):
    id = pw.PrimaryKeyField()
    telegram_id = pw.IntegerField()
    minitoken = pw.CharField(null=True)
    role = pw.CharField()

    class Meta:
        database = pw.SqliteDatabase(db_source) 
        table_name = 'Users'
        
class Notification(pw.Model):
    id = pw.PrimaryKeyField()
    created_telegram_id = pw.IntegerField()
    text = pw.CharField()
    send_at_dt = pw.DateTimeField()

    class Meta:
        database = pw.SqliteDatabase(db_source)
        table_name = 'Notifications'


class DBClient:
    name = ""

    def __init__(self, db_name):
        self.name = db_name
        User.create_table()
        Notification.create_table()
        
    def save_user(self, tg_id: int, token: str, role: str) -> None:
        try:
            if User.select().where(User.telegram_id == tg_id):
                user = User.select().where(User.telegram_id == tg_id).get()
                user.minitoken = token
                user.role = role
            else:
                user = User(telegram_id=tg_id, minitoken=token, role=role)
            user.save()
        except:
            pass # logging

    def get_minitoken(self, tg_id) -> None:
        try:
            result = User.select().where(User.telegram_id == tg_id).get().minitoken
            return result
        except:
            pass # logging
            
    def create_notification(self, tg_id, text, send_at_dt) -> None:
        try:
            notif = Notification(created_telegram_id=tg_id, text=text, send_at_dt=send_at_dt)
            notif.save()
        except:
            pass
    
    def get_my_notifications(self, tg_id) -> list:
        try:
            return [notif for notif in Notification.select().where(Notification.created_telegram_id == tg_id)]
        except:
            pass
        
    def get_user_role(self, tg_id) -> Union[str, None]:
        try:
            return User.select().where(User.telegram_id == tg_id).get().role
        except:
            pass
    
    def del_from_users(self, tg_id) -> None:
        try:
            User.delete().where(User.telegram_id == tg_id).execute()
        except:
            pass
        
    def get_all_students(self) -> list:
        try:
            return [user for user in User.select().where(User.role == 'student')]
        except:
            pass
        
    def get_all_notifications(self) -> list:
        try:
            return [notif for notif in Notification.select()]
        except:
            pass
        
    def del_notification():
        raise NotImplementedError