# Chat API

API для чатов и сообщений.

## Запуск

```bash
docker compose up --build
```

#### API: http://localhost:8000
#### Админка: http://localhost:8000/admin

(после запуска создать суперпользователя: ``` docker compose exec web python manage.py createsuperuser ```)

### API
#### Метод	Путь	Описание
#### POST	/chats/	Создать чат
#### POST	/chats/{id}/messages/	Отправить сообщение
#### GET	/chats/{id}/	Получить чат с сообщениями (?limit=20)
#### DELETE	/chats/{id}/delete/	Удалить чат


## Примеры запросов

### Создать чат
```bash
curl -X POST http://localhost:8000/chats/ -d "title=Тест"
```


## Отправить сообщение
```bash
curl -X POST http://localhost:8000/chats/3/messages/ -d "text=Привет"
```


## Получить чат
```bash
curl "http://localhost:8000/chats/3/?limit=5"
```


## Удалить чат
```bash
curl -X DELETE http://localhost:8000/chats/3/delete/
```


## Тесты

Проект включает 5 unit-тестов, покрывающих основные сценарии API:

```bash
# Запуск тестов
docker compose exec web python manage.py test
```


