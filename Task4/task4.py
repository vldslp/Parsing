import datetime
import pandas as pd
import requests
from lxml import html
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/114.0.0.0 YaBrowser/23.7.1.1140 Yowser/2.5 Safari/537.36'}

resp_mailru = requests.get("https://news.mail.ru/", headers=headers)
resp_lenta = requests.get("https://lenta.ru/", headers=headers)
resp_dzen = requests.get("https://dzen.ru/news?issue_tld=ru&utm_referrer=dzen.ru/", headers=headers)

dom1 = html.fromstring(resp_mailru.text)
dom2 = html.fromstring(resp_lenta.text)
dom3 = html.fromstring(resp_dzen.text)

# Сбор основных новостей с титульной страницы news.mail.ru
news = []

items = dom1.xpath("//div[contains(@class, 'newsitem')] | "
                   "//ul[contains(@class, 'list')]//span[contains(@class, 'item')]")

for item in items:
    new = {}
    link = item.xpath(".//a[contains(@class, 'newsitem')]/@href | "
                      ".//a[contains(@class, 'list')]/@href")
    name = item.xpath(".//a[contains(@class, 'newsitem')]//text() | "
                      ".//a[contains(@class, 'list')]//text()")
    tme = item.xpath(".//@datetime")
    if link or name != []:
        new['name'] = name
        new['link'] = link
        new['time'] = tme if tme != [] else str(datetime.datetime.now())
        news.append(new)

bases = []

for i in news:
    base = {}
    name, link, time = i.values()
    base['name'] = ''.join(name)
    base['link'] = ''.join(link)
    base['time'] = ''.join(time)
    bases.append(base)
print(bases)

bases = pd.DataFrame(bases)

print(bases.head())
pprint(len(news))


# Вывод результата поиска в файл
def save_to(base, news_file):
    base.to_csv(news_file, index=False, sep=';', encoding='utf-8')


save_to(bases, 'mailru_news.csv')



# Сбор основных новостей с титульной страницы lenta.ru
# news = []
#
# items = dom2.xpath("//a[contains(@class, 'card')]")
#
# for item in items:
#
#     new = {}
#     link = item.xpath("./@href")
#     pprint(link)
#     if str(link).split()[0] == "/":
#         link = 'https://lenta.ru/{}'.format(link)
#     name = dom2.xpath("./div[contains(@class, 'titles')]/h3/text()")
#     tme = item.xpath("./div[contains(@class, 'info')]/time[@class]/text()")
#     new['name'] = name
#     new['link'] = link
#     new['time'] = tme
#     news.append(new)
# pprint(news)
# bases = []
#
# for i in news:
#     base = {}
#     name, link, time = i.values()
#     base['name'] = ''.join(name)
#     base['link'] = ''.join(link)
#     base['time'] = ''.join(time)
#     bases.append(base)
#
#
# bases = pd.DataFrame(bases)
#
# print(bases.head())
# pprint(len(news))















# Сбор основных новостей с титульной страницы dzen.ru
#
# news = []
#
# items = dom3.xpath("//div[contains(@class, 'mg-card')]")
# print(items)
# for item in items:
#     new = {}
#     link = item.xpath(".//h2//a/@href")
#
#     name = item.xpath(".//h2//a//text()")
#     source = item.xpath(".//div[contains(@class, 'mg-card-footer')]//a/text()")
#     time = str(datetime.date.today()) + ':' + item.xpath(".//span[contains(@class, 'time')]/text()")
#     if link or name != []:
#         new['name'] = name
#         new['source'] = source
#         new['link'] = link
#         new['time'] = time
#
#         news.append(new)
#
# bases = []
#
# for i in news:
#     base = {}
#     name, source, link, time = i.values()
#     base['name'] = ''.join(name)
#     base['source'] = ''.join(source)
#     base['link'] = ''.join(link)
#     base['time'] = ''.join(time)
#     bases.append(base)
# print(bases)
#
# bases = pd.DataFrame(bases)
#
# print(bases.head())
# pprint(len(news))
