import sqlite3

def create_connection():
    conn = sqlite3.connect('weather.db')
    return conn

def create_table():
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                UTCDateTime TEXT NOT NULL,
                temperature REAL,
                humity REAL,
                pressure REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
def insert_weather(weather_data):
    conn = create_connection()

    for i in range(40):
        UTCDateTime = weather_data['list'][i]['dt_txt']
        temperature = round(weather_data['list'][i]['main']['temp'] - 273.15, 1)
        pressure = weather_data['list'][i]['main']['pressure']
        humity = weather_data['list'][i]['main']['humidity']
   
        # Verificar se o UTCDateTime já existe no banco de dados
        with conn:
            cursor = conn.execute('''
                SELECT COUNT(*) FROM weather WHERE UTCDateTime = ?
            ''', (UTCDateTime,))
            result = cursor.fetchone()

        # Se o UTCDateTime não existir, insere o registro
        if result[0] == 0:
            with conn:
                conn.execute('''
                    INSERT INTO weather (UTCDateTime, temperature, pressure, humity)
                    VALUES (?, ?, ?, ?)
                ''', (UTCDateTime, temperature, pressure, humity))
        else:
            print(f'Duplicado: O UTCDateTime {UTCDateTime} já existe no banco de dados.')

def get_all_weather():
    conn = create_connection()
    cursor = conn.execute('SELECT UTCDateTime, temperature, pressure, humity FROM weather')
    return cursor.fetchall()
