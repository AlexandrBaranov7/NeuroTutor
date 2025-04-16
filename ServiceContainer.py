from telebot import types, TeleBot
from environs import Env
from dbclient import DBClient as DB
from UrfuApiClient import UrfuApiClient

class ServiceContainer:
    def __init__(self, env_file: str = 'env.env'):
        env = Env()
        env.read_env(env_file)

        self.token: str = env('TG_BOT_TOKEN')
        self.admin_id: str = env('ADMIN_ID')
        self.bot: TeleBot = TeleBot(self.token)
        self.db: DB = DB('users')
        self.api: UrfuApiClient = UrfuApiClient()

service_instance = ServiceContainer()