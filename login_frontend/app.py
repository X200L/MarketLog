from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
import sqlite3
import hashlib
from cryptography.fernet import Fernet

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS content (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             idblock TEXT,
             short_title TEXT,
             img TEXT,
             altimg TEXT,
             title TEXT,
             contenttext TEXT,
             author TEXT,
             timestampdata DATETIME)''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT)''')
conn.close()

app = Flask(__name__)
TheKey=Fernet.generate_key()
app.secret_key = str(TheKey)
print(TheKey)
Valid = False
def create_user(username, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Добавление нового пользователя
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

def get_db_connection():
    
    
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/templates/<path:path>')
def logo(path):
    print(path)
    return send_from_directory('templates', path)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None # обнуляем переменную ошибок 
    if request.method == 'POST':
        username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

        # устанавливаем соединение с БД
        conn = get_db_connection() 
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        # закрываем подключение БД
        conn.close() 
        
        # теперь проверяем если данные сходятся формы с данными БД
        if user and user['password'] == hashed_password:
            # в случае успеха создаем сессию в которую записываем id пользователя
            session['user_id'] = user['id']
            # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
            return redirect('http://127.0.0.1:5000/')

        else:
            error = 'Неправильное имя пользователя или пароль'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def reg():
    error = None # обнуляем переменную ошибок 
    if request.method == 'POST':
        username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
        password2 = request.form['password2']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256
        if password == password2 and password !="" and username !="":
            Valid = True
            # Замените 'admin' и 'your_password' на желаемые имя пользователя и пароль
            create_user(username, password)
            return redirect('http://127.0.0.1:5001/login')

        # устанавливаем соединение с БД
        conn = get_db_connection() 
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        # закрываем подключение БД
        conn.close() 
        
        # теперь проверяем если данные сходятся формы с данными БД
        if user and user['password'] == hashed_password:
            # в случае успеха создаем сессию в которую записываем id пользователя
            session['user_id'] = user['id']
            # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
            return redirect('http://127.0.0.1:5000/')
        

        else:
            error = 'Неправильное имя пользователя или пароль'

    return render_template('reg.html', error=error)


if __name__ == '__main__':
    app.run(port=5001)