# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import yadisk
from os import environ
from pprint import pprint

# Для безопасности токен прописан в окружение исполняемого файла
token = environ['token']

#  Выведем первые 8 символов токена в лог-файл:
with open('log.txt', 'w') as log:
    rsl = 'Токен (первые 8 символов): ' + str(token)[:8] + '...\n'
    log.write(rsl)

# Инициализация доступа к API Yandex disk:
y = yadisk.YaDisk(token=token)

# Проверка работоспособности токена:

def result(result):     # Запись результата в лог-файл
    with open('log.txt', 'a') as log:
        log.write(result)
    print(result)

if y.check_token() == True:
    result('Проверка токена пройдена\n')
else:
    result('Проверка токена не пройдена')
    exit()

# Создание папок:
def create_folder(path):
    if not y.is_dir(path):
        y.mkdir(path)
        result(f'\nПапка "{path}" создана\n')
    else:
        result(f'\nПапка "{path}" уже существует\n')

# Создадим папку 'Test' в корне облачного диска:
create_folder('/Test')

# Загрузим 'test.txt' в папку 'Test':
y.upload("test.txt", "/Test/test1.txt")
result('Файл "/Test/test1.txt" создан\n')

# Листинг папки:
def dir_list(path):
    rs = f'Содержимое папки "..{path}":\n'
    i = 1
    for item in y.listdir(path):
        rs += f"{i}" + 45 * '-' + \
              f"\nИмя: {item['name']}\n" + \
              f"Размер: {item['size']} байт\n" + \
              f"Объект: {item['type']}\n" + \
              f"Тип объекта: {item['media_type']}\n" + \
              f"Дата создания: {item['created']}\n"
        i += 1
    result(rs)

# Получим содержимое папки 'Test':
dir_list('/Test')

# Создадим папку 'Hello Word' внутри папки 'Test':
create_folder('/Test/Hello Word')

#Загрузим 'test.txt' в 'Hello Word':
y.upload("test.txt", "/Test/Hello Word/test2.txt")
result('Файл "/Test/Hello Word/test2.txt" создан\n')

# Получим содержимое папки 'Hello Word':
dir_list('/Test/Hello Word')

# Удаление ранее созданного:
y.remove("/Test", permanently=True)
result('\nВсе ранее созданное удалено. \n')

dir_list('/')

