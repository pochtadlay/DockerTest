from flask import Flask, jsonify, render_template
import requests
import os
import psycopg2
from psycopg2 import sql
from datetime import datetime

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Функция для подключения к БД
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Инициализация таблицы при запуске

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # принудительно обновлять шаблоны, УБРАТЬ ИЗ РАБОЧЕЙ ВЕРСИИ!!!

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/vue')
def vue_page():
    return render_template('vue_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random')
def get_random():
    response = requests.get("http://random-service:5001/generate")  # Обратите внимание на имя сервиса!
    data = response.json()
    number = data['number']
    
    # Сохраняем в базу данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO random_numbers (number) VALUES (%s)",
        (number,)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"number": number, "saved_to_db": True})
@app.route('/list')
def get_last_numbers():
    # Получаем последние 5 чисел из БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT number, created_at FROM random_numbers ORDER BY created_at DESC LIMIT 5"
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    # Форматируем результат
    numbers = [
        {"number": row[0], "created_at": row[1].isoformat()} 
        for row in results
    ]
    
    return jsonify(numbers)

# Разделение для production/development
if __name__ == '__main__':
    # Только для локальной разработки без Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Выполняется при импорте (в production с Gunicorn)
    # Можно добавить инициализацию БД
    pass