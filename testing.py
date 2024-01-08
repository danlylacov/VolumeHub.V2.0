import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_ADRESS = os.environ['API_ADRESS']

action_name = 'Татнефть '[:-1]

anomal_volume_notes = dict(requests.get(f'{API_ADRESS}/get_anomal_volumes').json())

figi = requests.get(f'{API_ADRESS}/get_figi_by_action_name/{action_name}').json()

book = requests.get(f'{API_ADRESS}/get_order_book_percent/{figi}').json()

print(anomal_volume_notes)
print(figi)
print(book)
print(book['ask'])

