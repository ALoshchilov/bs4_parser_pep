# Проект парсера документации Python

Парсер документов PEP — Python Enhancement Proposal с официального сайта python.org.

## Информация об авторе
[Александр Лощилов](mailto:loshchilov.aleksandr@gmail.com?subject=[GitHub]%20PEP%20parser)

## Примененный стек технологий
Python, BeautifulSoup

## Запуск проекта:
Склонирировать репозиторий удобным способом

Создать виртуальное окружение
```
python -m venv venv
```
Активировать виртуальное окружение

```
source venv/Scripts/activate
```

Установить зависимости
```
pip install -r requirements.txt
```

## Запуск парсера
Для использования парсера необходимо запустить файл main.py в папке ./src
```
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

## Параметры запуска парсера

### Обязательные параметры запуска

```
whats-new - парсинг и вывод списка изменений
```

```
latest-version - парсинг и вывод списка версий Python с ссылками на документацию
```

```
download - парсинг и выгрузка архива с документацией
```

```
pep - парсинг и вывод статусов документов PEP с подсчетом числа документов в каждом статусе
```

### Необязательные параметры запуска

```
-h, --help - справка
```

```
-c, --clear-cache - очистка кэша сессии
```

```
-o pretty, --output pretty - вывод результатов в табличном виде
```

```
-o file, --output file - вывод результатов в виде файла в папке ./results
```

```
whats-new - парсинг и вывод списка изменений
```

```
latest-version - парсинг и вывод списка версий Python с ссылками на документацию
```

```
download - парсинг и выгрузка архива с документацией
```

```
pep - парсинг и вывод статусов документов PEP с подсчетом числа документов в каждом статусе
```
