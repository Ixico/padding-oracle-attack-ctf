import json
import logging
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, g, make_response

from crypto import Cipher, password_authenticate

app = Flask(__name__)
cipher = Cipher('key.bin')
AUTH_COOKIE = 'x-auth'
EXPIRATION_FORMAT = "%Y-%m-%d %H:%M:%S"
with open("data.json", "r") as file:
    DATA = json.load(file)


@app.before_request
def authentication():
    auth = request.cookies.get(AUTH_COOKIE)
    if request.endpoint in ['login', 'index', 'static']:
        return
    if auth is None:
        return redirect(url_for('login')), 401
    login, expiration = cipher.decrypt(auth).split('|')
    if datetime.strptime(expiration, EXPIRATION_FORMAT) < datetime.now():
        return redirect(url_for('index')), 401
    g.user = get_user(login)


@app.errorhandler(Exception)
def handle(error):
    logging.error(error)
    return render_template('error.html', message=error), 500


def get_user(login):
    return next((user for user in DATA if user["login"] == login), None)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = get_user(username)
    if user is None:
        return render_template('login.html', error='Invalid username or password'), 401
    if password_authenticate(password, user['password']):
        response = make_response(redirect(url_for('dashboard')))
        expiration = (datetime.now() + timedelta(hours=1)).strftime(EXPIRATION_FORMAT)
        response.set_cookie(AUTH_COOKIE, cipher.encrypt(f"{username}|{expiration}"), httponly=True)
        return response
    return render_template('login.html', error='Invalid username or password'), 401


@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie(AUTH_COOKIE, '', expires=0)
    return response


@app.route('/dashboard')
def dashboard():
    print(g.user)
    return render_template('dashboard.html', user=g.user['login'], message=g.user['message'])


if __name__ == '__main__':
    app.run(debug=False)
