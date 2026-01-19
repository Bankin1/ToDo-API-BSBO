# ToDo API

REST API для управления задачами с использованием матрицы Эйзенхауэра.

## Технологии

- Python 3.13
- FastAPI 0.115.0
- SQLAlchemy 2.0.36
- PostgreSQL (Supabase)
- Pydantic 2.10.0

## Структура проекта

```
ToDo-API-BSBO/
├── main.py              # Точка входа
├── database.py          # Подключение к БД
├── schemas.py           # Pydantic схемы
├── models/
│   └── task.py          # SQLAlchemy модель
├── routers/
│   ├── tasks.py         # CRUD операции
│   └── stats.py         # Статистика
├── .env                 # Переменные окружения
└── requirements.txt
```

## Запуск

```bash
git clone https://github.com/Bankin1/ToDo-API-BSBO.git
cd ToDo-API-BSBO

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Создать .env файл с DATABASE_URL

uvicorn main:app --reload
```

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/v2`

| Метод  | Endpoint              | Описание                    |
|--------|-----------------------|-----------------------------|
| GET    | /tasks                | Все задачи                  |
| POST   | /tasks                | Создать задачу              |
| GET    | /tasks/{id}           | Задача по ID                |
| PUT    | /tasks/{id}           | Обновить задачу             |
| PATCH  | /tasks/{id}/complete  | Отметить выполненной        |
| DELETE | /tasks/{id}           | Удалить задачу              |
| GET    | /tasks/search?q=      | Поиск                       |
| GET    | /tasks/quadrant/{Q}   | Фильтр по квадранту         |
| GET    | /tasks/status/{s}     | Фильтр по статусу           |
| GET    | /stats                | Статистика                  |

**Дополнительно:**
- `GET /` — информация об API
- `GET /health` — проверка здоровья
- `GET /docs` — Swagger документация

## Автор

Бандуков Илья, БСБО-12-22
