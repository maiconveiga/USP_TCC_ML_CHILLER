import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&lang=pt_br&appid={API_KEY}'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()  # Retorna os dados de clima
    else:
        return None
