# Главный файл приложения
from fastapi import FastAPI
from routers import tasks, stats

app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={
    "name": "Бандуков Илья БСБО-12-22"
    }
)

app.include_router(tasks.router)
app.include_router(stats.router)


@app.get("/")
async def welcome() -> dict:
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
        "contact": app.contact
    }


@app.post("/tasks")
async def create_task(task: dict):
    return {"message": "Запись успешно создана!", "task": task}
