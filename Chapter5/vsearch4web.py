from time import sleep
from flask import Flask, render_template, request, session, copy_current_request_context
from vsearch import search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in
from threading import Thread

app = Flask(__name__)

app.secret_key = 'VeryHardKey'

app.config['dbconfig'] = {"host": "127.0.0.1",
                          "user": "vsearch",
                          "password": "vsearchpasswd",
                          "database": "vsearchlogDB"}


@app.route('/search4', methods=["POST"])
def do_search() -> 'html':
    @copy_current_request_context
    def log_request(req: "flask_request", res: str) -> None:
        sleep(15)
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
                        (phrase, letters, ip, browser_string, results)
                        values
                        (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form["phrase"], req.form["letters"],
                                  req.remote_addr, req.user_agent.browser, res))

    phrase = request.form["phrase"]
    letters = request.form["letters"]
    title = "Ваши результаты"
    result = str(search4letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, result))
        t.start()
        #log_request(request, result)
    except Exception as err:
        print('Не удалось обновить лог журнала')

    return render_template("result.html", the_title=title, the_phrase=phrase,
                           the_letters=letters, the_result=result)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template("entry.html", the_title="Добро пожаловать на тестирование функции searv4letters в web")


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    contents = []
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
                        from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
    except ConnectionError as err:
        print('Подключение к БД присутствует?')
    except CredentialsError as err:
        print('Пользователь/пароль некорректен')
    except SQLError as err:
        print('Ваш запрос корректен?')
    except Exception as err:
        print(str(err))

    titles = ('Строка', 'Фраза', 'Ip адрес', ',Браузер', 'Результат')
    return render_template("viewlog.html",
                           the_title="Лог выполнения",
                           the_row_titles=titles,
                           the_data=contents)


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'Теперь вы в системе'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'Вы теперь не в системе'


if __name__ == "__main__":
    app.run(debug=True)
