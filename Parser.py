from bs4 import BeautifulSoup
import requests
from pprint import pprint
from DBcm import UseDatabase

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

    def __init__(self, local):
        self.url = 'http://sitv.ru'
        self.path = '/home/anton/Sitv/'
        self.local = local

    # возвращает текст основной страницы
    def get_main_page(self) -> str:
        if self.local:
            with open(self.path + "main.html") as f:
                return f.read()
        else:
            s = requests.Session()
            page = s.get(self.url, headers=Sitv.prop, cookies=Sitv.cookies)
            return page.text

    def get_url(self, data, index=0):
        url = ""
        if self.local:
            return self.path + str(index) + ".html"
        else:
            return 'https://sitv.ru' + data.findNext('a').get('href')

    def get_news(self, save=False) -> set:
        result = {}
        allNews = []
        self.main = self.get_main_page()

        if len(self.main) != 0:
            s = requests.Session()
            soup = BeautifulSoup(self.main, 'lxml')  #"html.parser")
            index = 0
            for data in soup.findAll('div', {'class': ['mlenta']}):
                index += 1
                url = self.get_url(data, index)
                one_news = News(data.findNext('a').text, url, self.local)
                result[data.findNext('span').text] = one_news

                # value.append(data.findNext('a').text)
                # value.append('https://sitv.ru/' + data.findNext('a').get('href'))
                # filteredNews[data.findNext('span').text] = value
        return result

    def save_page(self):
        s = requests.Session()
        page = s.get(self.url, headers=Sitv.prop, cookies=Sitv.cookies)
        with open(self.path + "main.html", 'w') as f:
            f.write(page.text)


if __name__ == '__main__':
    """ это код для сохранения локальной копии
    sitv = Sitv(False)
    index = 0
    for k, v in sitv.get_news().items():
        index += 1
        v.save_page('/home/anton/Sitv/' + str(index) + ".html")
        # print(k, v, v.get_url())
        #v.get_article()
        # pprint(v.get_article())
    sitv.save_page()
    """

    sitv = Sitv(False)
    for k, v in sitv.get_news().items():
        # v.get_article()
        pprint(v.get_article())
        break


# pprint(sitv.get_news())
