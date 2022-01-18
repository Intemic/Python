from flask import Flask, session

app = Flask(__name__)

app.secret_key = 'VerySecretKey'

@app.route('/setuser/<user>')
def setuser(user: str) -> str:
    session['user'] = user
    return 'Значение пользователя установлено в :' + session['user']

@app.route('/getuser')
def getuser() -> str:
    return 'Текущее значение пользователя :' + session['user']

if __name__ == '__main__':
    app.run()