Пример приложения, которое периодически парсит главную страницу ​Hacker News,​ вытягивая из нее список постов и сохраняя в базу данных.
Приложение имеет HTTP API с одним методом (​GET /​posts) для получения списка новостей.

### Запуск приложения
Перед запуском необходимо создать .env файл с переменными окружения, пример файла - env.example

База данных, приложение и процесс парсинга запускается через docker-compose:
```
docker-compose build
docker-compose up -d 
```
Пример запроса:
```
curl -X GET http://localhost:8000/posts 
curl -X GET http://localhost:8000/posts?order=title:asc&limit=10&offset=10
```
Пример ответа:
```
[
    {
        "id": 1,
        "title": "Arm is offering early-stage startups free access to its chip designs",
        "url": "https://techcrunch.com",
        "created": "2020-05-01T11:47:03.465663"
    },
    {
        "id": 2,
        "title": "A Survey on Tree Edit Distance and Related Problems (2005) [pdf]",
        "url": "https://grfia.dlsi.ua.es/",
        "created": "2020-05-01T11:47:03.391926"
    }
]
```
Каждые 10 минут в базу данных добавляются новые новости

Диапазон допустимых значений параметров limit, offset: 0..30

## Запуск тестов

```
docker-compose -f docker-compose.tests.yml build
docker-compose -f docker-compose.tests.yml up 
docker-compose -f docker-compose.tests.yml down
```