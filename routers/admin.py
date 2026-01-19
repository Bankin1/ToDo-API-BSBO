from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_async_session
from models import User, Task
from dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def get_all_users(
    db: AsyncSession = Depends(get_async_session),
    current_admin: User = Depends(get_current_admin)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    users_with_tasks = []
    for user in users:
        tasks_result = await db.execute(
            select(func.count(Task.id)).where(Task.user_id == user.id)
        )
        tasks_count = tasks_result.scalar()
        
        users_with_tasks.append({
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email,
            "role": user.role,
            "tasks_count": tasks_count
        })
    
    return {
        "total_users": len(users_with_tasks),
        "users": users_with_tasks
    }

