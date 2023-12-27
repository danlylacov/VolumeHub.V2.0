
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ContentType
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv.main import load_dotenv

from adminDB import UsersDataBase
from keyboards import start_keyboard, payment_keyboard, PRICES_FOR_PAYMENT
from apsched import send_message_interval
from volume_analyze.Standard_deviation_and_Z_score.stream_analyze import StandartDeviationAnalize

load_dotenv()
API_TOKEN = os.environ['BOT_TOKEN']
PAYMENT_TOKEN = os.environ['PAYMENT_TOKEN']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db = UsersDataBase()
    db.add_user(userid=message.from_user.id, username=message.from_user.username)
    await bot.send_message(message.chat.id, "Привет! Это бот VolumeHub", reply_markup=start_keyboard)


@dp.message_handler(content_types=['text'])
async def menu(message: types.Message):
    if message.text == 'ℹО ботеℹ':
        db = UsersDataBase()
        await bot.send_message(message.chat.id, str(db.get_about_bot_text()))

    if message.text == '📌Подписка📌':
        db = UsersDataBase()
        await bot.send_message(message.chat.id, str(db.get_subscription_text()), reply_markup=payment_keyboard)


@dp.callback_query_handler(lambda c: c.data)
async def get_payment_link(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == '30':
        await bot.send_invoice(callback_query.from_user.id,
                               title="Подписка на бота",
                               description='подписка на получение аномальных объемов на 30 дней',
                               provider_token=PAYMENT_TOKEN,
                               currency='rub',
                               is_flexible=False,
                               prices=[PRICES_FOR_PAYMENT[0]],
                               start_parameter="one-month",
                               payload='30_days')
    elif callback_query.data == '90':
        await bot.send_invoice(callback_query.from_user.id,
                               title="Подписка на бота",
                               description='подписка на получение аномальных объемов на 90 дней',
                               provider_token=PAYMENT_TOKEN,
                               currency='rub',
                               is_flexible=False,
                               prices=[PRICES_FOR_PAYMENT[1]],
                               start_parameter="one-month",
                               payload='90_days')
    elif callback_query.data == '365':
        await bot.send_invoice(callback_query.from_user.id,
                               title="Подписка на бота",
                               description='подписка на получение аномальных объемов на 365 дней',
                               provider_token=PAYMENT_TOKEN,
                               currency='rub',
                               is_flexible=False,
                               prices=[PRICES_FOR_PAYMENT[2]],
                               start_parameter="one-month",
                               payload='365_days')
    elif callback_query.data == 'test':
        db = UsersDataBase()
        subscription = db.get_subscription(callback_query.from_user.id)
        if subscription == '-':
            db.give_subscription_to_user(30, callback_query.from_user.id)
            await bot.send_message(callback_query.from_user.id, "Пробный период на 30 дней активирован!")
        else:
            await bot.send_message(callback_query.from_user.id, "Вы уже активировали пробный период!")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    print(pre_checkout_q)
    db = UsersDataBase()
    prices = db.get_prices()
    db.add_payment(int(pre_checkout_q.id), int(pre_checkout_q.from_user.id), pre_checkout_q.from_user.first_name, pre_checkout_q.from_user.username,
                   pre_checkout_q.from_user.language_code, pre_checkout_q.currency, int(pre_checkout_q.total_amount)//100)
    if str(pre_checkout_q.total_amount // 100) == prices[0]:
        db.give_subscription_to_user(30, int(pre_checkout_q.from_user.id))
    if str(pre_checkout_q.total_amount // 100) == prices[1]:
        db.give_subscription_to_user(90, int(pre_checkout_q.from_user.id))
    if str(pre_checkout_q.total_amount // 100) == prices[2]:
        db.give_subscription_to_user(365, int(pre_checkout_q.from_user.id))
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succsessful_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Платеж выполнен!')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    deviation = StandartDeviationAnalize()
    result = deviation.analize()
    await bot.send_message(691902762, result)


# Функция для отправки сообщения через бота
async def send_message_to_user(chat_id, text, photo_path=None):
    if photo_path:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id, photo, caption=text, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN)


async def on_startup(dp):
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()
    print('Scheduler started!')





if __name__ == "__main__":

    while True:
        try:
            executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
        except:
            print('rebooting bot...')
