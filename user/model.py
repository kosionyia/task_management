from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    username: str = Field(max_length=128)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, pattern=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')  # At least one letter and one number
    age: int = Field(ge=16, lt=85)

