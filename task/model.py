from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, EmailStr


class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    status: Status 

class TaskResponse(TaskCreate):
    id: str
    user_id: EmailStr

