from datetime import datetime
import pandas as pd
import requests
from lxml import html
from pprint import pprint
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/114.0.0.0 YaBrowser/23.7.1.1140 Yowser/2.5 Safari/537.36'}


# Функция получения DOM
def dom(site):
    response = requests.get(site, headers=headers)
    d = html.fromstring(response.text)
    return d


site = 'https://news.mail.ru/'

# Сбор основных новостей с титульной страницы news.mail.ru
links = []

items = dom(site).xpath("//div[contains(@class, 'newsitem')] | "
                        "//ul[contains(@class, 'list')]//span[contains(@class, 'item')]")

for item in items:
    link = item.xpath(".//a[contains(@class, 'newsitem')]/@href | "
                      ".//a[contains(@class, 'list')]/@href")
    if link:
        links.append(link[0])

bases = []

for i in links:
    item = dom(i).xpath("//div[@data-news-id]")

    name = item[0].xpath(".//h1/text()")
    intro = item[0].xpath(".//div[contains(@class, 'intro')]/p/text()")
    date = item[0].xpath(".//span[@datetime]/@datetime")
    source = item[0].xpath(".//span[@class='note']/a//text()")
    source_link = item[0].xpath(".//span[@class='note']/a/@href")

    base = {
        'name': ''.join(name),
        'intro': ''.join(intro),
        'link': i,
        'time': ''.join(date),
        'source': ''.join(source),
        'source_link': ''.join(source_link)
    }

    bases.append(base)
    time.sleep(0.2)

pprint(bases)

bases = pd.DataFrame(bases)

pprint(bases.head())
pprint(bases.info)


# Вывод результата поиска в файл
def save_to(base, news_file):
    base.to_csv(news_file, index=False, sep=';', encoding='utf-8')


save_to(bases, 'mail_news.csv')


# Сбор новостей с титульной страницы lenta.ru
news = []
mon = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

site = 'https://lenta.ru/'

items = dom(site).xpath("//a[contains(@class, 'card')]")

for item in items:

    new = {}
    link = item.xpath("./@href")

    if link[0][0] == "/":
        link = 'https://lenta.ru{}'.format(link[0])
    else:
        link = link[0]

    name = item.xpath(".//h3/text()")
    tme = item.xpath(".//time/text()")

    # форматирование полученной даты новости
    # если есть только время, то добавляется текущая дата
    if tme == []:
        tme = datetime.now().strftime("%H:%M, %d.%m.%Y")
    elif len(str(tme)) < 10:
        tme = '{}, {}'.format(tme[0], datetime.now().strftime("%d.%m.%Y"))
    else:
        m = tme[0].split(',')
        n = m[1].split(' ')

        # Замена месяца на число
        for i in range(len(mon)):
            if n[2][:3] == mon[i]:
                n[2] = str(i + 1)
                d = datetime(int(n[3]), int(n[2]), int(n[1]))
        tme = m[0] + ', ' + str(d.strftime("%d.%m.%Y"))

    new['name'] = name
    new['link'] = link
    new['time'] = tme
    news.append(new)

bases = []

for i in news:
    base = {}
    name, link, time = i.values()
    base['name'] = ''.join(name)
    base['link'] = ''.join(link)
    base['time'] = time
    bases.append(base)

bases = pd.DataFrame(bases)

print(bases.head())
pprint(len(news))

save_to(bases, 'lenta_news.csv')
