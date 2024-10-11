from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file
from app.weather import get_weather
from app.models import insert_weather, get_all_weather

app = Flask(__name__)

# Endpoint para a interface HTML
@app.route('/')
def index():
    weather_data = get_all_weather()  # Busca os dados do banco de dados
    return render_template('index.html', weather_data=weather_data)

# Endpoint para coletar os dados do clima e salvar no banco
@app.route('/collect_weather', methods=['POST'])
def collect_weather():
    city = 'rio de janeiro'
    weather_data = get_weather(city)
    
    if weather_data:
        insert_weather(weather_data)
        return redirect(url_for('index'))
    else:
        return jsonify({"error": "Could not fetch weather data"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

