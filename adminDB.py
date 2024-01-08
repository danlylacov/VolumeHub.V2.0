import sqlite3
from datetime import datetime, timedelta

from dotenv.main import load_dotenv
import os


class UsersDataBase:

    def __init__(self):
        self.db = sqlite3.connect('/root/VolumeHub.V2.0/admin.db')
        self.cur = self.db.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            userid INTEGER,
                            username TEXT,
                            subscription TEXT)
                            """)
        self.db.commit()


    def add_user(self, userid, username):
        userids = self.cur.execute('SELECT userid FROM users').fetchall()
        if (userid,) not in userids:
            self.cur.execute('INSERT INTO users(userid, username, subscription) VALUES (?, ?, "-");',
                             (userid, username))
            self.db.commit()



    def get_userids(self):
        result = []
        userids = self.cur.execute('SELECT userid FROM users')
        for el in userids:
            try:
                result.append(int(el[0]))
            except:
                pass
        return result

    def get_subscriptors_ids(self):
        result = []
        users = self.cur.execute('SELECT userid, subscription FROM users').fetchall()
        for request in users:
            try:
                date_string = str(request[1])
                date_format = '%Y-%m-%d %H:%M:%S.%f'
                subscription_date = datetime.strptime(date_string, date_format)

                if datetime.now() < subscription_date:
                    result.append(int(request[0]))
            except:
                pass
        return list(set(result))

    def get_subscription(self, user_id):
        subscription = str(self.cur.execute(f"""SELECT subscription FROM users WHERE userid = {user_id}""").fetchone()[0])
        return subscription
    def give_subscription_to_user(self, interval_in_days: int, user_id: int):


        subscription = str(self.cur.execute(f"""SELECT subscription FROM users WHERE userid = {user_id}""").fetchone()[0])


        if subscription == "-":
            until = datetime.now() + timedelta(days=interval_in_days)
            self.cur.execute("UPDATE users SET subscription = ? WHERE userid = ?",
                             (until, user_id))
            self.db.commit()
        else:
            time_format = "%Y-%m-%d %H:%M:%S.%f"
            formatted_time = datetime.strptime(subscription, time_format)
            if formatted_time >= datetime.now():
                until = formatted_time + timedelta(days=interval_in_days)
                self.cur.execute("UPDATE users SET subscription = ? WHERE userid = ?",
                             (until, user_id))
                self.db.commit()
            if formatted_time < datetime.now():
                until = datetime.now() + timedelta(days=interval_in_days)
                self.cur.execute("UPDATE users SET subscription = ? WHERE userid = ?",
                             (until, user_id))
                self.db.commit()


    def get_Z(self):
        return float(self.cur.execute("""SELECT value FROM settings WHERE name = "Z_deviation";""").fetchone()[0])


    def update_Z(self, z):
        self.cur.execute(f'UPDATE settings SET value = {z} WHERE name = "Z_deviation";')
        self.db.commit()


    def get_about_bot_text(self):
        return str(self.cur.execute("""SELECT value FROM settings WHERE name = "about_bot_text";""").fetchone()[0])

    def update_about_bot_text(self, about: str):
        self.cur.execute(f'UPDATE settings SET value = "{about}" WHERE name = "about_bot_text";')
        self.db.commit()


    def get_prices(self):
        days30 = self.cur.execute("""SELECT value FROM settings WHERE name = "30_days";""").fetchone()[0]
        days90 = self.cur.execute("""SELECT value FROM settings WHERE name = "90_days";""").fetchone()[0]
        days365 = self.cur.execute("""SELECT value FROM settings WHERE name = "365_days";""").fetchone()[0]
        return [days30, days90, days365]


    def update_prices(self, days30, days90, days365):
        self.cur.execute(f'UPDATE settings SET value = "{days30}" WHERE name = "30_days";')
        self.cur.execute(f'UPDATE settings SET value = "{days90}" WHERE name = "90_days";')
        self.cur.execute(f'UPDATE settings SET value = "{days365}" WHERE name = "365_days";')
        self.db.commit()


    def get_subscription_text(self):
        return str(self.cur.execute("""SELECT value FROM settings WHERE name = "subscription_text";""").fetchone()[0])


    def update_subscription_text(self, text):
        self.cur.execute(f'UPDATE settings SET value = "{text}" WHERE name = "subscription_text";')
        self.db.commit()


    def add_payment(self, payment_id, from_id, first_name, username, language_code, currency, total_amount):
        self.cur.execute("""INSERT INTO payments(paymentId, fromId, firstName, username, languadeCode, currency, totalAmount) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (payment_id, from_id, first_name,username, language_code, currency, total_amount))
        self.db.commit()





