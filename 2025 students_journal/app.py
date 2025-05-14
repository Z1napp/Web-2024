from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import redis
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Redis-клієнт
r = redis.Redis(host='redis', port=6379, decode_responses=True)

DB_PATH = 'instance/users.db'

def init_db():
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (login, email, password, role) VALUES (?, ?, ?, ?)",
                      (login, email, password, role))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Користувач з таким логіном або email вже існує"
        finally:
            conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        cached_user = r.get(f"user:{login}")
        if cached_user:
            user = json.loads(cached_user)
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login = ?", (login,))
            row = c.fetchone()
            conn.close()
            if row:
                user = {'id': row[0], 'login': row[1], 'password': row[3], 'role': row[4]}
                r.set(f"user:{login}", json.dumps(user), ex=3600)
            else:
                user = None

        if user and check_password_hash(user['password'], password):
            session['user'] = user['login']
            session['role'] = user['role']
            return f"Вітаю, {user['login']}! Ваша роль: {user['role']}"
        return "Невірний логін або пароль"
    return render_template('login.html')

@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
