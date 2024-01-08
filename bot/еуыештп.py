import requests


stocks = list(requests.get('http://127.0.0.1:8000/get_hour_data/BBG006L8G4H1').json())
print(stocks)