from bs4 import BeautifulSoup
import requests
from pprint import pprint
from DBcm import UseDatabase
from datetime import datetime, date, timedelta

# одна новость
class News:
    def __init__(self, title: str, url: str, local):
        self.title = title
        self.url = url
        self.local = local

    def __str__(self):
        return self.title

    def get_title(self) -> str:
        return self.title

    def get_url(self) -> str:
        return self.url

    def get_article(self) -> str:
        if self.local:
            with open(self.url) as f:
                page_text = f.read()
        else:
            ns = requests.Session()
            page_text = ns.get(self.url, headers=Sitv.prop, cookies=Sitv.cookies).text

        if len(page_text) != 0:
            result = ""
            soup = BeautifulSoup(page_text, 'lxml')  #"html.parser")
            # заголовок
            tag_head = soup.find('h1', attrs={"itemprop" : "headline"})
            if tag_head is not None:
                #del tag_head["itemprop"]
                #result = "<strong><ins>" + str(tag_head.text) + "</ins></strong>" + '\n\n'
                result = "<span class =""tg-spoiler"">" + str(tag_head.text) + "</span>" + '\n\n'


            # текстовка
            tag_div = soup.findAll('div', {'class': ['mtxt']})[0]
            for elem in tag_div.contents:
                if elem.name == 'span':
                    result = result + str(elem.text)
                elif elem.name == 'br':
                    result = result + '\n'
                else:
                    if elem.find('&nbsp;') != -1:
                        elem.replace_with(' ')
                    result = result + str(elem)
        return result

    def get_image(self):
        pass

    def save_page(self, fname : str):
        s = requests.Session()
        page = s.get(self.url, headers=Sitv.prop, cookies=Sitv.cookies)
        with open(fname, 'w') as f:
            f.write(page.text)
            print('Страница - ' + self.url + 'сохранена как : ' + fname)


class Sitv:
    prop = {
        'User-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}
    cookies = {'_ga': 'GA1.2.1868264853.1606921345', }
    main = ""
    # параметры BD
    dbconfig = {"host": "127.0.0.1",
                "user": "sitv",
                "password": "sitvpass",
                "database": "sitvDB"}

    def __init__(self):
        self.url = 'http://sitv.ru'
        self.path = '/home/anton/Sitv/'
        self.news = {}

    def get_sql_prev_date_time(self) -> str:
        # отмотаем на день назад
        result = {}
        prev_date = datetime.today() - timedelta(days=1)
        result['date'] = prev_date.strftime('%Y-%m-%d')
        result['time'] = prev_date.strftime('%H:%M')
        return result

    # загрузка статей с сайта
    def load_from_site(self) -> bool:
        # result = False
        # session = requests.Session()
        # req_main_page = session.get(self.url, headers=Sitv.prop, cookies=Sitv.cookies)
        # # все ок, разбираем на запчасти
        # if req_main_page.status_code == 200:
            #pass
            # проверим наличие в БД

        sql_date_time = self.get_sql_prev_date_time()
        with UseDatabase(Sitv.dbconfig) as cursor:
            _SQL = """select * from news_head where dt >= %s
                                                and tm >= %s"""
            cursor.execute(_SQL,  (sql_date_time['date'], sql_date_time['time']))
            for row in cursor.fetchall():
                print(row)

            # soup = BeautifulSoup(self.main, 'lxml')
            # for data in soup.findAll('div', {'class': ['mlenta']}):
            #     url = 'https://sitv.ru' + data.findNext('a').get('href')
            #     one_news = News(data.findNext('a').text, url)
            #     result[data.findNext('span').text] = one_news

    # загрузка статей из БД
    def load_from_db(self):
        pass

    # сохранение в БД
    def save_to_db(self):
        pass

sitv = Sitv()
sitv.load_from_site()