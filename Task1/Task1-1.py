# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

url = 'https://api.github.com/users'
user = 'vldslp'
var = 'repos'

# Получаем развернутую информацию по репозиториям пользователя:
response = requests.get(f'{url}/{user}/{var}')
j_data = response.json()

# Извлекаем названия репозиториев:
repos = []
for i in range(len(j_data)):
    repos.append(j_data[i]['name'])

pprint(repos)

# Выводим полученный список в .json:
name = user + '_repos.json'

with open(name, "w") as f_obj:
    json.dump(repos, f_obj)