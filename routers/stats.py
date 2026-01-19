from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Task

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
async def get_stats(db: AsyncSession = Depends(get_db)) -> dict:
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
