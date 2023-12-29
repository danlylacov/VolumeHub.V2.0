import sqlite3
from datetime import datetime
from dotenv.main import load_dotenv
import os


class DataBase(object):

    def __init__(self):
        try:
            load_dotenv()
            PATH = os.environ['DB_PATH']
            self.db = sqlite3.connect('../../VolumeHub.V2.0/stocks.db')
            self.cur = self.db.cursor()
            print('Database connected!')

        except:
            raise ValueError('Name of database is incorrect!')


    def get_historic_data(self, figi: str): # -> list
        '''
        функция получения исторических данных по акции в виде списка
        :param figi: figi-индефикатор акции
        :return: список с историческими данными
        '''
        action_volume = []
        volumes = self.cur.execute(f'SELECT volume FROM {figi}')
        for el in volumes:
            action_volume.append(int(el[0]))
        return action_volume


    def get_figis(self): # -> list
        '''
        Функция получения всех figi из бд
        :return: список с figi
        '''
        result = []
        request = self.cur.execute('SELECT figi FROM FIGI;')
        for el in request:
            result.append(str(el[0]))
        return result


    def get_action_names(self): # -> list
        '''
        Функция получения всех названий акций
        :return: список с названиями акций
        '''
        result = []
        request = self.cur.execute('SELECT name FROM FIGI;')
        for el in request:
            result.append(str(el[0]))
        return result


    def get_action_name_by_figi(self, figi: str): # -> str
        '''
        функция получения названия акции по ее figi
        :param figi: figi-идентификатор акции
        :return: название акции
        '''
        request = self.cur.execute(f'SELECT name FROM FIGI WHERE figi = "{figi}"').fetchone()[0]
        return request


    def get_figi_by_action_name(self, name: str): # -> str
        '''
        Функция получение figi-идентификатора акции по её названию
        :param name: название акции
        :return: figi-идентификатор
        '''
        request = self.cur.execute(f'SELECT figi FROM FIGI WHERE name = "{name}";').fetchone()[0]
        return request

    def insert_data(self, figi: str, data_dict: dict):

        self.cur.execute(f"INSERT INTO {figi}(open, high, low, close, volume, time)  VALUES (?, ?, ?, ?, ?, ?);", (int(data_dict['open']), int(data_dict['high']), int(data_dict['low']), int(data_dict['close']), int(data_dict['volume']), str(data_dict['time'])))
        self.db.commit()


    def delete_first_candle(self, figi: str):
        self.cur.execute(f'DELETE FROM {figi}  WHERE id IN (SELECT id FROM {figi} LIMIT 1);')
        self.db.commit()


    def test(self):
        return self.cur.execute('SELECT min(id) FROM BBG000BX7DH0').fetchone()

    def get_price_change(self, figi: str):
        request = self.cur.execute(f'SELECT open, close FROM {figi} WHERE id = (SELECT max(id) FROM {figi});').fetchone()
        open, close = request[0], request[1]
        return round((float(close)/float(open)) * 100 - 100, 3)

    def get_last_price(self, figi: str):
        request = self.cur.execute(f'SELECT close FROM {figi} WHERE id = (SELECT max(id) FROM {figi});').fetchone()[0]
        return request

    def get_last_volume(self, figi: str):
        request = self.cur.execute(f'SELECT volume FROM {figi} WHERE id = (SELECT max(id) FROM {figi});').fetchone()[0]
        return request


    def get_day_change(self, figi: str):
        year = datetime.utcnow().year
        month = datetime.utcnow().month
        day = datetime.utcnow().day
        print(year, month, day)
        open_day_price = int(self.cur.execute(f"""SELECT open FROM {figi} WHERE time LIKE '{year}-{month}-{day}%' """).fetchone()[0])
        last_price = int(self.cur.execute(f"""SELECT close FROM {figi} WHERE id = (SELECT max(id) FROM {figi})""").fetchone()[0])
        return round((last_price / open_day_price) * 100 - 100, 3)

    def get_hour_data(self, figi: str):
        data = self.cur.execute(f"""SELECT * FROM {figi} ORDER BY id DESC LIMIT 60""").fetchall()[::-1]
        return data




db = DataBase()
print(db.get_hour_data('BBG000BX7DH0'))

















