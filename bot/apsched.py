from aiogram import Bot
from volume_analyze.Standard_deviation_and_Z_score.stream_analyze import StandartDeviationAnalize
from db import DataBase
from datetime import datetime
from adminDB import UsersDataBase


db = DataBase()
users_db = UsersDataBase()

async def send_message_interval(bot: Bot):
    print('Sched func works!')
    deviation = StandartDeviationAnalize()
    result = deviation.analize()
    for i in range(len(result)):
        if result[i][1][0] == True:
            print(users_db.get_subscriptors_ids())
            for chat_id in users_db.get_subscriptors_ids():

                await bot.send_message(chat_id,
                                   "🛑\n" +

                                   str(db.get_action_name_by_figi(result[i][0])).upper() +
                                   "\n\n"+str(db.get_price_change(result[i][0])) + "% - изменение цены\n" +
                                   str(db.get_day_change(result[i][0])) + "% - изменение за день\n" +
                                    str(db.get_last_price(result[i][0])) + " ₽ - текущая цена\n"+
                                   str(db.get_last_volume(result[i][0])) + " кол-во лот - объём\n" +
                                   "\nВремя (" + str(int(datetime.utcnow().hour) + 3) + ":" + str(datetime.utcnow().minute) + ")" + str(datetime.utcnow()).split(' ')[0] +
                                    "\n\nЗамечено ботом @volumeHub_bot")