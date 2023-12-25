from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from adminDB import UsersDataBase

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_buttons = [
    KeyboardButton(text='ℹО ботеℹ'),
    KeyboardButton(text='📌Подписка📌')
]
start_keyboard.add(*start_buttons)



payment_keyboard = InlineKeyboardMarkup(row_width=1)
db = UsersDataBase()
prices = db.get_prices()
payment_buttons = [
    InlineKeyboardButton(text=f"30 дней  | пробный период", callback_data="test"),
    InlineKeyboardButton(text=f"30 дней  | {prices[0]} рублей", callback_data="30"),
    InlineKeyboardButton(text=f"90 дней  | {prices[1]} рублей", callback_data="90"),
    InlineKeyboardButton(text=f"365 дней | {prices[2]} рублей", callback_data="365"),
]
payment_keyboard.add(*payment_buttons)


PRICES_FOR_PAYMENT = [
    LabeledPrice(label="Подписка на бота", amount=int(prices[0])*100),
    LabeledPrice(label="Подписка на бота", amount=int(prices[1])*100),
    LabeledPrice(label="Подписка на бота", amount=int(prices[2])*100),
]

