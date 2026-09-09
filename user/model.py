from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    username: str = Field(max_length=128)
    email: EmailStr

class UserCreate(UserBase):
    age: int = Field(ge=16, lt=85)

