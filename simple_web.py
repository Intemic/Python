from flask import Flask, session
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'SuperCode'


@app.route('/')
def hello() -> str:
    return 'Привет из простого web приложения'


@app.route('/page1')
@check_logged_in
def page1() -> str:
    return 'Страница 1'


@app.route('/page2')
@check_logged_in
def page2() -> str:
    return 'Страница 2'


@app.route('/page3')
@check_logged_in
def page3() -> str:
    return 'Страница 3'


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'Теперь вы в системе'



@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'Вы теперь не в системе'

if __name__ == '__main__':
    app.run()
