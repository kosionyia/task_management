from datetime import datetime, timezone
from typing import TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from task.schema import Task



class User(SQLModel, table=True):
    username: str = Field(unique= True, max_length=128)
    email: EmailStr = Field(primary_key=True)
    age: int = Field(ge=16, lt=85)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tasks: list["Task"] = Relationship(back_populates="user")