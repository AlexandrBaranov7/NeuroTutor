import sqlite3

class DBClient:

    db_name = ""

    def __init__(self, name):
        self.db_name = name

    def db_create(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Создаем таблицу Users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
        telegram_id TEXT NOT NULL,
        minitoken TEXT NOT NULL,
        UNIQUE (telegram_id)
        )
        ''')

        connection.commit()
        connection.close()

    def set_data(self, tg_id, minitoken):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Добавляем tg_id и минитокен в бд
        cursor.execute(f'''
            INSERT OR REPLACE INTO Users (telegram_id, minitoken) 
            VALUES ({tg_id}, {minitoken});
            ''')

        connection.commit()
        connection.close()
    def get_minitoken(self, tg_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Получаем минитокен пользователся с telegramg_id = tg_id
        cursor.execute(f'''
            SELECT minitoken from Users
            WHERE telegram_id = {tg_id}
            ''')

        result = cursor.fetchone()[0]

        connection.commit()
        connection.close()
        return result

