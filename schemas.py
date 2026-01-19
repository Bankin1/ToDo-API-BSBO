from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    is_important: bool = Field(..., description="Важность задачи")


class TaskCreate(TaskBase):
    deadline_at: datetime = Field(..., description="Дедлайн задачи")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_important: Optional[bool] = Field(None)
    deadline_at: Optional[datetime] = Field(None)
    completed: Optional[bool] = Field(None)


class TaskResponse(TaskBase):
    id: int
    quadrant: str
    is_urgent: bool = Field(description="Срочность (рассчитывается автоматически)")
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime]
    deadline_at: Optional[datetime]
    days_until_deadline: Optional[int] = Field(None, description="Дней до дедлайна")

    class Config:
        from_attributes = True
