import os
from aiogram import Bot, types
from datetime import datetime
from dotenv import load_dotenv
from adminDB import UsersDataBase
import requests
from make_image.image_maker import ImageMaker




load_dotenv()
API_ADRESS = os.environ['API_ADRESS']



async def send_message_interval(bot: Bot):
    print('Sched func works!')
    print(datetime.utcnow())
    anomal_volume_notes = dict(requests.get(f'{API_ADRESS}/get_anomal_volumes').json())
    users_db = UsersDataBase()

    for id in anomal_volume_notes.keys():

        note = anomal_volume_notes[id]
        action_name = str(note['action_name'])
        price_change = str(note['price_change'])
        day_price_change = str(note['day_price_change'])
        price = str(note['price'])
        volume = str(note['volume'])
        time = str(note['time'])
        if float(price_change) >= 0:
            amoj = '📈'
        else:
            amoj = '📉'

        figi = requests.get(f'{API_ADRESS}/get_figi_by_action_name/{action_name[:-1]}').json()


        book = requests.get(f'{API_ADRESS}/get_order_book_percent/{figi}').json()
        ask, bid = book['ask'], book['bid']

        ImageMaker(figi, action_name, '', price, volume, str(int(volume) * float(price)), day_price_change,
                   price_change, ask, bid)

        for chat_id in users_db.get_subscriptors_ids():
            photo_path = 'result.png'
            with open(photo_path, 'rb') as photo:
                await bot.send_photo(chat_id=chat_id,
                                     caption= amoj + "\n" +
                                             action_name.upper() +
                                             "\n\n" + price_change + "% - изменение цены\n" +
                                             day_price_change + "% - изменение за день\n" +
                                             price + " ₽ - текущая цена\n" +
                                             volume + " кол-во лот - объём\n" +
                                             "\nВремя: " + time +
                                             "\n\nЗамечено ботом @volumeHub_bot",
                                     photo=types.InputFile(photo))

        requests.get(f'{API_ADRESS}/delete_anomal_volume/{id}')


async def subscription_reminder(bot: Bot):
    print('dvedfvefr')
    users_db = UsersDataBase()
    for id in users_db.get_subscriptors_ids():
        if id != '-':
            date_str = users_db.get_subscription(id).split('.')[0]
            print(date_str)
            date_format = "%Y-%m-%d %H:%M:%S"
            subscription_datetime = datetime.strptime(date_str, date_format)
            remaining_subscription_in_days = int(str(subscription_datetime - datetime.now()).split(' ')[0])
            print(remaining_subscription_in_days)
            if remaining_subscription_in_days < 3:
                await bot.send_message(id,
                                       f'❗️❗️❗\nВнимание!\nВаша подписка истекает {subscription_datetime.date()}.\nПродлите её сейчас, чтобы и дальше получать уведомления об аномальных объемах!')



















