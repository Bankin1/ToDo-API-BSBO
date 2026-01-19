# ToDo API

REST API для управления задачами с использованием матрицы Эйзенхауэра. Позволяет организовывать задачи по квадрантам важности и срочности.

## Технологии

- Python 3.13
- FastAPI 0.115.0
- Uvicorn 0.32.0
- Pydantic 2.10.0
- SQLAlchemy 2.0.36
- PostgreSQL (Supabase)
- asyncpg 0.30.0

## Структура проекта

```
ToDo-API-BSBO/
├── main.py           # Главный файл приложения
├── database.py       # Настройка подключения к БД
├── schemas.py        # Pydantic модели
├── models/
│   └── task.py       # SQLAlchemy модель Task
├── routers/
│   ├── tasks.py      # Endpoints для задач
│   └── stats.py      # Endpoints для статистики
├── .env              # Переменные окружения (не в git)
└── requirements.txt
```

## Запуск

```bash
# Клонировать репозиторий
git clone https://github.com/Bankin1/ToDo-API-BSBO.git
cd ToDo-API-BSBO

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать файл .env с переменными окружения

# Проверить подключение к БД
python test_connection.py

# Запустить сервер
uvicorn main:app --reload
```

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/v1`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /tasks | Получить все задачи |
| POST | /tasks | Создать задачу |
| GET | /tasks/{id} | Получить задачу по ID |
| PUT | /tasks/{id} | Обновить задачу |
| PATCH | /tasks/{id}/complete | Отметить выполненной |
| DELETE | /tasks/{id} | Удалить задачу |
| GET | /tasks/stats | Статистика по задачам |
| GET | /tasks/search?keyword= | Поиск задач |
| GET | /tasks/quadrant/{Q1-Q4} | Фильтр по квадранту |
| GET | /tasks/status/{status} | Фильтр по статусу |

Документация Swagger: http://127.0.0.1:8000/docs

## Автор

Бандуков Илья, БСБО-12-22
