import re
import sqlite3
import os.path
from user_class import User
from datetime import datetime

DATABASE_PATH = "./users_db.db"

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_db = os.path.join(THIS_FOLDER, DATABASE_PATH)

class SQLighter:
    def __init__(self):
        self.connection = sqlite3.connect(my_db,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self,user_chat_id):
        with self.connection:
            data = self.cursor.execute(f"SELECT * from users_table WHERE user_chat_id = {user_chat_id}")
            result = data.fetchone()
            if result is None:
                return False
            else:
                return True

    def user_get_all(self,user_chat_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users_table WHERE user_chat_id = {user_chat_id}")
            user = self.cursor.fetchone()
            return user

    def add_user_id(self,user_chat_id):
        with self.connection:
            date_time_str = "01/01/1970 00:00:00"
            return self.cursor.execute(f"INSERT INTO users_table (user_chat_id, user_name, user_last_name, user_phone_number, user_test_time, user_test_result) VALUES (?, ?, ?, ?, ?, ?)", (user_chat_id, "A", "B", "C", date_time_str , 0))
             
    def add_user_name(self,user_chat_id,user_name):
        with self.connection:
            return self.cursor.execute(f"UPDATE users_table SET user_name = ? WHERE {user_chat_id}",(user_name, ))

    def add_user_last_name(self,user_chat_id,user_last_name):
        with self.connection:
            return self.cursor.execute(f"UPDATE users_table SET user_last_name = ? WHERE {user_chat_id}",(user_last_name, ))

    def add_user_phone_number(self,user_chat_id,user_phone_number):
        with self.connection:
            return self.cursor.execute(f"UPDATE users_table SET user_phone_number = ? WHERE {user_chat_id}",(user_phone_number, ))

    def add_user_test_time(self,user_chat_id,user_test_time):
        with self.connection:
            return self.cursor.execute(f"UPDATE users_table SET user_test_time = ? WHERE {user_chat_id}",(user_test_time, ))
    
    def add_user_test_result(self,user_chat_id,user_test_result):
        with self.connection:
            return self.cursor.execute(f"UPDATE users_table SET user_test_result = ? WHERE {user_chat_id}",(user_test_result, ))

    # def update_user(self,user_chat_id,user_test_result,user_test_time):
    #     with self.connection:
    #         return self.cursor.execute(f"UPDATE users_table SET user_test_result = (?), user_test_time = (?) WHERE {user_chat_id}",(user_test_result, user_test_time))

    def close_db(self):
        self.connection.close()
