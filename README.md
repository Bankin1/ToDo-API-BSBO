# ToDo API

REST API для управления задачами с использованием матрицы Эйзенхауэра. Позволяет организовывать задачи по квадрантам важности и срочности.

## Технологии

- Python 3.13
- FastAPI 0.115.0
- Uvicorn 0.32.0
- Pydantic 2.10.0

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

# Запустить сервер
uvicorn main:app --reload
```

API будет доступен по адресу: http://127.0.0.1:8000

Документация Swagger: http://127.0.0.1:8000/docs

## Автор

Бандуков Илья, БСБО-12-22