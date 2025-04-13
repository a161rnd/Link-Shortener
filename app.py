from flask import Flask, redirect, request, jsonify, render_template
import sqlite3
import secrets

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                      (short_code TEXT PRIMARY KEY, original_url TEXT)''')
    conn.commit()
    conn.close()

# Генерация короткого кода (6 символов)
def generate_short_code():
    return secrets.token_urlsafe(4)[:6]

# Главная страница с формой
@app.route('/')
def home():
    return '''
    <h1>Сервис коротких ссылок</h1>
    <form action="/shorten" method="post">
        <input type="text" name="url" placeholder="Введите URL" required>
        <button type="submit">Сократить</button>
    </form>
    '''

# Создание короткой ссылки
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')
    if not original_url:
        return "Ошибка: URL не указан", 400
    
    short_code = generate_short_code()
    
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (short_code, original_url))
    conn.commit()
    conn.close()
    
    return f'''
    <h2>Ваша короткая ссылка:</h2>
    <a href="/{short_code}">http://ваш-домен.ру/{short_code}</a>
    '''

# Перенаправление по короткой ссылке
@app.route('/<short_code>')
def redirect_to_original(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    else:
        return "Ссылка не найдена", 404

if __name__ == '__main__':
    init_db()
    app.run()