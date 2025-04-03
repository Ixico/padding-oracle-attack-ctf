from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, g, make_response
from crypto import Cipher

app = Flask(__name__)
cipher = Cipher('key.bin')
AUTH_COOKIE = 'x-auth'
EXPIRATION_FORMAT = "%Y-%m-%d %H:%M:%S"

@app.before_request
def authentication():
    auth = request.cookies.get(AUTH_COOKIE)
    if request.endpoint in ['login', 'index']:
        return
    if auth is None:
        return redirect(url_for('login')), 401
    g.auth, expiration = cipher.decrypt(auth).split('|')
    if datetime.strptime(expiration, EXPIRATION_FORMAT) < datetime.now():
        return redirect(url_for('index')), 401


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        response = make_response(redirect(url_for('dashboard')))
        expiration = (datetime.now()+ timedelta(hours=1)).strftime(EXPIRATION_FORMAT)
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
    return render_template('dashboard.html', user=g.auth)


if __name__ == '__main__':
    app.run(debug=True)
