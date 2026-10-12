from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


Priority = Literal["low", "medium", "high"]


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=5000)
    priority: Priority = "medium"
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=5000)
    priority: Priority | None = None
    completed: bool | None = None
    due_date: datetime | None = None


class TaskRead(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskPage(BaseModel):
    items: list[TaskRead]
    total: int
    skip: int
    limit: int
