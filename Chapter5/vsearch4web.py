from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector

app = Flask(__name__)


def log_request(req: "flask_request", res: str) -> None:
    with open("vsearch.log", 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


def log_db(req: "flask_request", res: str) -> None:
    dbconfig = {"host": "127.0.0.1",
                "user": "vsearch",
                "password": "vsearchpasswd",
                "database": "vsearchlogDB"}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form["phrase"], req.form["letters"], req.remote_addr, req.user_agent.browser, res))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search4', methods=["POST"])
def do_search() -> 'html':
    phrase = request.form["phrase"]
    letters = request.form["letters"]
    title = "Ваши результаты"
    result = str(search4letters(phrase, letters))
    log_request(request, result)

    log_db(request, result)
    return render_template("result.html", the_title=title, the_phrase=phrase,
                           the_letters=letters, the_result=result)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template("entry.html", the_title="Добро пожаловать на тестирование функции searv4letters в web")



@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open("vsearch.log") as log:
        for line in log:
            spisok = escape(line).split('|')
            contents.append(spisok)
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template("viewlog.html",
                           the_title="Лог выполнения",
                           the_row_titles=titles,
                           the_data=contents)


if __name__ == "__main__":
    app.run(debug=True)