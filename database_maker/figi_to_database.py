import sqlite3
import os
from dotenv.main import load_dotenv

load_dotenv()
PATH = os.environ['DB_PATH']
bd = sqlite3.connect('../VolumeHub.V2.0/stocks.db') # подключение к бд
cur = bd.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS FIGI('
            'figi TEXT,'
            'name TEXT);')
bd.commit()



def figi_to_bd():
    f = open('figi.txt', 'r', encoding='utf-8').readlines()
    for figis in f:
        figi = figis.split()[0]
        name = ''
        for i in range(1, len(figis.split())):
            name+=figis.split()[i] + ' '
        cur.execute('INSERT INTO FIGI VALUES(?,?);', (figi, name))
        bd.commit()


if __name__ == '__main__':
    figi_to_bd()
