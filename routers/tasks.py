from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import get_db
from models import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def get_all_tasks(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return {
        "count": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    }


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)) -> TaskResponse:
    if task.is_important and task.is_urgent:
        quadrant = "Q1"
    elif task.is_important and not task.is_urgent:
        quadrant = "Q2"
    elif not task.is_important and task.is_urgent:
        quadrant = "Q3"
    else:
        quadrant = "Q4"

    new_task = Task(
        title=task.title,
        description=task.description,
        is_important=task.is_important,
        is_urgent=task.is_urgent,
        quadrant=quadrant,
        completed=False
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    if "is_important" in update_data or "is_urgent" in update_data:
        if task.is_important and task.is_urgent:
            task.quadrant = "Q1"
        elif task.is_important and not task.is_urgent:
            task.quadrant = "Q2"
        elif not task.is_important and task.is_urgent:
            task.quadrant = "Q3"
        else:
            task.quadrant = "Q4"

    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task.completed = True
    task.completed_at = datetime.now()

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    await db.delete(task)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/stats")
async def get_tasks_stats(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Task))
    tasks = result.scalars().all()

    by_quadrant = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    completed = 0
    pending = 0

    for task in tasks:
        by_quadrant[task.quadrant] += 1
        if task.completed:
            completed += 1
        else:
            pending += 1

    return {
        "total_tasks": len(tasks),
        "by_quadrant": by_quadrant,
        "by_status": {
            "completed": completed,
            "pending": pending
        }
    }


@router.get("/search")
async def search_tasks(keyword: str, db: AsyncSession = Depends(get_db)) -> dict:
    if len(keyword) < 2:
        raise HTTPException(
            status_code=400,
            detail="Ключевое слово должно содержать минимум 2 символа"
        )

    result = await db.execute(select(Task))
    tasks = result.scalars().all()

    filtered_tasks = [
        task.to_dict()
        for task in tasks
        if keyword.lower() in task.title.lower() or
           (task.description and keyword.lower() in task.description.lower())
    ]

    if not filtered_tasks:
        raise HTTPException(
            status_code=404,
            detail="Задачи не найдены"
        )

    return {
        "query": keyword,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }


@router.get("/status/{status}")
async def get_tasks_by_status(status: str, db: AsyncSession = Depends(get_db)) -> dict:
    if status not in ["completed", "pending"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный статус. Используйте: completed, pending"
        )

    is_completed = status == "completed"
    result = await db.execute(select(Task).where(Task.completed == is_completed))
    tasks = result.scalars().all()

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="Задачи не найдены"
        )

    return {
        "status": status,
        "count": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    }


@router.get("/quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str, db: AsyncSession = Depends(get_db)) -> dict:
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4"
        )

    result = await db.execute(select(Task).where(Task.quadrant == quadrant))
    tasks = result.scalars().all()

    return {
        "quadrant": quadrant,
        "count": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    }


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int, db: AsyncSession = Depends(get_db)) -> TaskResponse:
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task
