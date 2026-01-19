from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import List
from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import get_async_session
from models import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

URGENCY_THRESHOLD_DAYS = 3


def calculate_urgency(deadline_at: datetime) -> bool:
    if not deadline_at:
        return False
    days_left = (deadline_at.replace(tzinfo=None) - datetime.now()).days
    return days_left <= URGENCY_THRESHOLD_DAYS


def calculate_quadrant(is_important: bool, is_urgent: bool) -> str:
    if is_important and is_urgent:
        return "Q1"
    elif is_important and not is_urgent:
        return "Q2"
    elif not is_important and is_urgent:
        return "Q3"
    else:
        return "Q4"


def calculate_days_until_deadline(deadline_at: datetime) -> int | None:
    if not deadline_at:
        return None
    return (deadline_at.replace(tzinfo=None) - datetime.now()).days


def task_to_response(task: Task) -> dict:
    is_urgent = calculate_urgency(task.deadline_at)
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_important": task.is_important,
        "is_urgent": is_urgent,
        "quadrant": calculate_quadrant(task.is_important, is_urgent),
        "completed": task.completed,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
        "deadline_at": task.deadline_at,
        "days_until_deadline": calculate_days_until_deadline(task.deadline_at)
    }


@router.get("", response_model=List[TaskResponse])
async def get_all_tasks(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return [task_to_response(t) for t in tasks]


@router.get("/quadrant/{quadrant}", response_model=List[TaskResponse])
async def get_tasks_by_quadrant(
    quadrant: str,
    db: AsyncSession = Depends(get_async_session)
):
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException(status_code=400, detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4")
    
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    
    filtered = [task_to_response(t) for t in tasks if task_to_response(t)["quadrant"] == quadrant]
    return filtered


@router.get("/search", response_model=List[TaskResponse])
async def search_tasks(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_async_session)
):
    keyword = f"%{q.lower()}%"
    result = await db.execute(
        select(Task).where(
            (Task.title.ilike(keyword)) | (Task.description.ilike(keyword))
        )
    )
    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(status_code=404, detail="По данному запросу ничего не найдено")
    return [task_to_response(t) for t in tasks]


@router.get("/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(
    status: str,
    db: AsyncSession = Depends(get_async_session)
):
    if status not in ["completed", "pending"]:
        raise HTTPException(status_code=400, detail="Недопустимый статус. Используйте: completed или pending")
    is_completed = (status == "completed")
    result = await db.execute(select(Task).where(Task.completed == is_completed))
    tasks = result.scalars().all()
    return [task_to_response(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task_to_response(task)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_session)
):
    is_urgent = calculate_urgency(task.deadline_at)
    quadrant = calculate_quadrant(task.is_important, is_urgent)

    new_task = Task(
        title=task.title,
        description=task.description,
        is_important=task.is_important,
        quadrant=quadrant,
        completed=False,
        deadline_at=task.deadline_at
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return task_to_response(new_task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    is_urgent = calculate_urgency(task.deadline_at)
    task.quadrant = calculate_quadrant(task.is_important, is_urgent)

    await db.commit()
    await db.refresh(task)
    return task_to_response(task)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    deleted_info = {"id": task.id, "title": task.title}
    await db.delete(task)
    await db.commit()

    return {"message": "Задача успешно удалена", **deleted_info}


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task.completed = True
    task.completed_at = datetime.now()

    await db.commit()
    await db.refresh(task)
    return task_to_response(task)
