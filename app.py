from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

FILENAME = 'user.txt'
LOGFILE = 'login_activity.txt'

def load_username(filename):
    users = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    username, password = parts
                    users[username] = password
    except FileNotFoundError:
        pass
    return users

def save_user(username, password):
    with open(FILENAME, 'a') as file:
        file.write(f"{username},{password}\n")

def write_login_log(username):
    with open(LOGFILE, 'a') as log_file:
        log_file.write(f"User {username} login successfully.\n")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = load_username(FILENAME)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error="Username already taken.")
        save_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_username(FILENAME)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            return render_template('login.html', error="Username not found.")
        if users[username] != password:
            return render_template('login.html', error="Incorrect password.")
        write_login_log(username)
        return render_template('welcome.html', username=username)
    return render_template('login.html')

@app.route('/users')
def show_users():
    users = load_username(FILENAME)
    return render_template('users.html', users=users)

@app.route('/developer', methods=['GET', 'POST'])
def developer():
    if request.method == 'POST':
        dev_pass = request.form['password']
        if dev_pass != '123456':
            return render_template('developer.html', error="Wrong password.")
        users = load_username(FILENAME)
        logs = []
        if os.path.exists(LOGFILE):
            with open(LOGFILE, 'r') as file:
                logs = file.readlines()
        return render_template('developer_panel.html', users=users, logs=logs)
    return render_template('developer.html')

if __name__ == '__main__':
    app.run(debug=True)