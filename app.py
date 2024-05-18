from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Database initialization
conn = sqlite3.connect('todo.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS tasks 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, task TEXT, due_date TEXT, category TEXT, completed INTEGER)''')
conn.commit()

# Routes

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id == 'admin':
            c.execute("SELECT tasks.*, users.username FROM tasks JOIN users ON tasks.user_id = users.id")
            tasks = c.fetchall()
            return render_template('admin_todo.html', tasks=tasks, user_id=user_id)
        else:
            c.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
            tasks = c.fetchall()
            return render_template('index.html', tasks=tasks, user_id=user_id)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['user_id'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('index'))
        else:
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        user_id = session['user_id']
        task = request.form['task']
        due_date = request.form['due_date']
        category = request.form['category']
        completed = 0
        c.execute("INSERT INTO tasks (user_id, task, due_date, category, completed) VALUES (?, ?, ?, ?, ?)",
                  (user_id, task, due_date, category, completed))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/add_user_task', methods=['POST'])
def add_user_task():
    if 'user_id' in session and session['user_id'] == 'admin':
        user_id = request.form['user_id']
        task = request.form['task']
        due_date = request.form['due_date']
        category = request.form['category']
        completed = 0
        c.execute("INSERT INTO tasks (user_id, task, due_date, category, completed) VALUES (?, ?, ?, ?, ?)",
                  (user_id, task, due_date, category, completed))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    if 'user_id' in session:
        c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_completed_tasks', methods=['POST'])
def delete_completed_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        c.execute("DELETE FROM tasks WHERE user_id=? AND completed=1", (user_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/registered_users')
def registered_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        return render_template('registered_users.html', users=users)
    return redirect(url_for('index'))

@app.route('/view_other_users')
def view_other_users():
    if 'user_id' in session and session['user_id'] == 'admin':
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        return render_template('registered_users.html', users=users)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
