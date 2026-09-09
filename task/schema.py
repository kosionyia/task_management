from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from task.model import Status
from user.schema import User


class Task(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=256)
    description: str
    status: Status = Field(sa_column_kwargs={"default": "todo"})

    user_id: EmailStr = Field(foreign_key="user.email", nullable=False)

    user: "User" = Relationship(back_populates="tasks")