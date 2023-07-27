import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import pandas as pd
from pandas.api.types import is_numeric_dtype

# Запуск клиента сервера Mongo и создание БД
client = MongoClient('127.0.0.1', 27017)

db = client['hh_ru']
vacancys = db.vacancys

# Задание оригинального индекса коллекции
vacancys.create_index([('Vacancy_id', pymongo.ASCENDING)], name='search_index', unique=True)

vacancy = {}

# Чтение файла с результатами поиска (из предыдущего дом.задания)
path = '../Task2/Result/{}'.format('vacancies.csv')
df = pd.read_csv(path, sep=';')


# Функция добавления новой записи в базу с проверкой на оригинальность
def ins_db(param):
    try:
        vacancys.insert_one(param)
    except DuplicateKeyError:
        print(f'Запись с таким id:{vacancy.get("_id")} уже есть!')


# Перенос найденных вакансий в базу vacancies
for i in df.index:                          # Перебор вакансий (строк)
    for k in df.columns:                    # Перебор критериев (столбцов)
        if is_numeric_dtype(df[k].loc[i]):
            vacancy[k] = int(df[k].loc[i])  # переход из 'numpy.int64' в int
        else:
            vacancy[k] = df[k].loc[i]
    print(i)
    ins_db(vacancy)                         # Проверка на оригинальность и добавление в базу
    vacancy = {}

print(vacancys.find({'Vacancy_id': 8396403}))


# Функция поиска вакансий с попаданием в вилку предлагаемых зарплат
def salary(size):
    c = []
    for d in vacancys.find({
                            '$and': [
                                {"Salary_min": {'$lte': size}},
                                {"Salary_max": {'$gte': size}}
                                ]
                            }):
        c.append(d)
    return pd.DataFrame(c)


# Желаемая зарплата
like = 80000

# Результат поиска с выводом на экран
p = salary(like)
head = p.columns.drop('_id')
print(p[head])

# Вывод результата поиска в файл
path = '../Task2/Result/{}'.format('vacancies_like.csv')
p.to_csv(path, index= False, sep=';', encoding='utf-8')