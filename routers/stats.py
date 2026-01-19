from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from models import Task, User
from database import get_async_session
from dependencies import get_current_user

router = APIRouter(prefix="/stats", tags=["statistics"])

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


@router.get("/")
async def get_tasks_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    if current_user.role == "admin":
        result = await db.execute(select(Task))
    else:
        result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    
    tasks = result.scalars().all()

    total_tasks = len(tasks)
    by_quadrant = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    by_status = {"completed": 0, "pending": 0}

    for task in tasks:
        is_urgent = calculate_urgency(task.deadline_at)
        quadrant = calculate_quadrant(task.is_important, is_urgent)
        by_quadrant[quadrant] += 1
        
        if task.completed:
            by_status["completed"] += 1
        else:
            by_status["pending"] += 1

    return {
        "total_tasks": total_tasks,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }


@router.get("/deadlines")
async def get_deadlines_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> dict:
    if current_user.role == "admin":
        result = await db.execute(select(Task).where(Task.completed == False))
    else:
        result = await db.execute(
            select(Task).where(
                (Task.user_id == current_user.id) & (Task.completed == False)
            )
        )
    
    tasks = result.scalars().all()

    deadlines = []
    for task in tasks:
        days_left = None
        if task.deadline_at:
            days_left = (task.deadline_at.replace(tzinfo=None) - datetime.now()).days

        deadlines.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "deadline_at": task.deadline_at,
            "days_until_deadline": days_left
        })

    deadlines.sort(key=lambda x: x["days_until_deadline"] if x["days_until_deadline"] is not None else 9999)

    return {
        "pending_tasks": len(deadlines),
        "tasks": deadlines
    }
