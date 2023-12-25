from dotenv.main import load_dotenv
import os
from datetime import timedelta
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now
import sqlite3


class HistoricalDataParser(object):

    def __init__(self, file_name: str):
        load_dotenv()
        self.TOKEN = os.environ['TINKOFF_API_TOKEN'] # токен TinkoffAPI
        self.file_name = file_name
        load_dotenv()
        PATH = os.environ['DB_PATH']
        self.bd = sqlite3.connect(PATH)
        self.cur = self.bd.cursor()



    def get_candels(self, figi: str):  # str, str -> .txt
        f'''
        функция получения свечей акции интервалом 5 мин за 60 последних дней по figi
        :param figi: figi-номер акции по которой необходимо получение данных
        :param file_name: название файла .txt в который необходимо записать данные
        :return: file_name.txt

        !!!ВАЖНО: в свече указано время по часовому поясу UTC+00.00
        '''
        self.cur.execute(f"""  
                 CREATE TABLE IF NOT EXISTS {figi}(
                 id integer primary key autoincrement,
                 open TEXT,
                 high TEXT,
                 low TEXT,
                 close TEXT,
                 volume TEXT,
                 time TEXT); """)
        self.bd.commit()
        with Client(self.TOKEN) as client:
            for candle in client.get_all_candles(
                    figi=figi,
                    from_=now() - timedelta(days=7),
                    interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
            ):
                self.cur.execute(f"""INSERT INTO {figi} (open, high, low, close, volume, time) VALUES (?,?,?,?,?,?)""",
                                 (float(candle.open.units) + (candle.open.nano /1000000000),
                                  float(candle.high.units) + (candle.high.nano /1000000000),
                                  float(candle.low.units) + (candle.low.nano /1000000000),
                                  float(candle.close.units) + (candle.close.nano /1000000000),
                                  candle.volume,
                                  candle.time)
                                 )
                self.bd.commit()
        print(f'{figi} успешно записан!')


    def run(self):  # None -> None
        '''
        Функция записи данных о свечах (интервал 5 мин, за последние 2 месяца) по акциям из файла figi.txt
        Выводит:
            {figi} успешно записан! - при успешной записи данных по инструменту
            {figi} не записан! - при ошибке
        :return: None
        '''
        f = open(self.file_name, 'r', encoding='utf-8').readlines()
        for i in range(len(f)):
            self.get_candels(f[i].split()[0])




if __name__ == '__main__':
    parse = HistoricalDataParser('figi.txt')
    parse.run()



