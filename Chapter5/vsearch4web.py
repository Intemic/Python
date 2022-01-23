from flask import Flask, render_template, request, session
from vsearch import search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'VeryHardKey'

app.config['dbconfig'] = {"host": "127.0.0.1",
                          "user": "vsearch",
                          "password": "vsearchpasswd",
                          "database": "vsearchlogDB"}


def log_request(req: "flask_request", res: str) -> None:
    with open("vsearch.log", 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


def log_db(req: "flask_request", res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form["phrase"], req.form["letters"],
                              req.remote_addr, req.user_agent.browser, res))


@app.route('/search4', methods=["POST"])
def do_search() -> 'html':
    phrase = request.form["phrase"]
    letters = request.form["letters"]
    title = "Ваши результаты"
    result = str(search4letters(phrase, letters))
    log_request(request, result)
    try:
        log_db(request, result)
    except ConnectionError as err:
        print(str(err))
    except CredentialsError as err:
        print(str(err))
    except Exception as err:
        print(str(err))

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
        print(str(err))
    except CredentialsError as err:
        print(str(err))
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
