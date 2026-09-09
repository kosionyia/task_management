from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

from task.schema import Task



class User(SQLModel, table=True):
    username: str = Field(unique= True, max_length=128)
    email: EmailStr = Field(primary_key=True)
    hashed_password: str
    age: int = Field(ge=16, lt=85)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tasks: list["Task"] = Relationship(back_populates="user")