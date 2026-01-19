# ToDo API

REST API для управления задачами с использованием матрицы Эйзенхауэра.

## Технологии

- Python 3.13
- FastAPI 0.115.0
- SQLAlchemy 2.0.36
- PostgreSQL (Supabase)
- Pydantic 2.10.0

## Особенности

- **Автоматический расчёт срочности**: если до дедлайна ≤ 3 дней — задача срочная
- **Динамический квадрант**: пересчитывается на основе важности и срочности
- **Статистика по дедлайнам**: отслеживание сроков невыполненных задач

## Структура проекта

```
ToDo-API-BSBO/
├── main.py
├── database.py
├── schemas.py
├── models/
│   └── task.py
├── routers/
│   ├── tasks.py
│   └── stats.py
└── requirements.txt
```

## Запуск

```bash
git clone https://github.com/Bankin1/ToDo-API-BSBO.git
cd ToDo-API-BSBO

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

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
| GET    | /stats                | Общая статистика            |
| GET    | /stats/deadlines      | Статистика по дедлайнам     |

## Пример создания задачи

```json
POST /api/v2/tasks/
{
  "title": "Сдать проект",
  "description": "Завершить разработку API",
  "is_important": true,
  "deadline_at": "2026-01-22T23:59:00"
}
```

## Автор

Бандуков Илья, БСБО-12-22
