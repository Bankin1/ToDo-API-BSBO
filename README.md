# ToDo API

REST API для управления задачами с использованием матрицы Эйзенхауэра и JWT-аутентификацией.

## Технологии

- Python 3.13
- FastAPI 0.115.0
- SQLAlchemy 2.0.36
- PostgreSQL (Supabase)
- JWT аутентификация (python-jose)
- Bcrypt хеширование паролей

## Структура проекта

```
ToDo-API-BSBO/
├── main.py
├── database.py
├── schemas.py
├── schemas_auth.py
├── auth_utils.py
├── dependencies.py
├── models/
│   ├── task.py
│   └── user.py
├── routers/
│   ├── tasks.py
│   ├── stats.py
│   ├── auth.py
│   └── admin.py
├── .env
└── requirements.txt
```

## Запуск

```bash
git clone https://github.com/Bankin1/ToDo-API-BSBO.git
cd ToDo-API-BSBO

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить .env файл с DATABASE_URL и SECRET_KEY

uvicorn main:app --reload
```

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/v3`

### Аутентификация
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /auth/register | Регистрация |
| POST | /auth/login | Вход |
| GET | /auth/me | Текущий пользователь |
| PATCH | /auth/change-password | Смена пароля |

### Задачи
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /tasks | Все задачи |
| POST | /tasks | Создать задачу |
| GET | /tasks/{id} | Задача по ID |
| PUT | /tasks/{id} | Обновить |
| DELETE | /tasks/{id} | Удалить |
| PATCH | /tasks/{id}/complete | Завершить |
| GET | /tasks/today | Задачи на сегодня |
| GET | /tasks/search?keyword= | Поиск |
| GET | /tasks/quadrant/{Q} | По квадранту |
| GET | /tasks/status/{s} | По статусу |

### Статистика
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /stats | Общая статистика |
| GET | /stats/deadlines | По дедлайнам |

### Администрирование
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | /admin/users | Список пользователей |

## Роли

- **user** — видит только свои задачи
- **admin** — видит все задачи всех пользователей

## Автор

Бандуков Илья, БСБО-12-22
