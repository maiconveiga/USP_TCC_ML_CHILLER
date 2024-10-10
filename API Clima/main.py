import requests
import pandas as pd
import openpyxl

API_KEY = 'af14a5d98cd1cc1fc38ce560697d2727'
city = 'rio de Janeiro'
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&lang=pt_br&appid={API_KEY}'

r = requests.get(url, verify=False)
r_dic = r.json()

data = []
total_items = len(r_dic['list'])

for i in range(total_items):
    timestamp = r_dic['list'][i]['dt_txt']
    temp = r_dic['list'][i]['main']['temp'] - 273.15
    temp_min = r_dic['list'][i]['main']['temp_min'] - 273.15
    temp_max = r_dic['list'][i]['main']['temp_max'] - 273.15
    pressao = r_dic['list'][i]['main']['pressure']
    umidade = r_dic['list'][i]['main']['humidity']
    descricao = r_dic['list'][i]['weather'][0]['main'] 
    vento_velocidade = r_dic['list'][i]['wind']['speed']  

    data.append([timestamp, temp, temp_min, temp_max, pressao, umidade, descricao, vento_velocidade])

df = pd.DataFrame(data, columns=['Data/Hora', 'Temperatura (°C)', 'Temp Mínima (°C)', 'Temp Máxima (°C)', 'Pressão (hPa)', 'Umidade (%)', 'Descrição', 'Velocidade vento (m/s)'])

df.to_excel('clima.xlsx')
