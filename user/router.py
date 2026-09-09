from fastapi import APIRouter, HTTPException

from db import SessionDep
from user.model import UserBase, UserCreate
from user.schema import User
from user.schema import User


router = APIRouter(prefix="/user")


@router.post("/", response_model=UserBase, status_code=201)
async def create_user(
    user: UserCreate,
    session: SessionDep
    ):

    _user = session.get(User, user.email)
    if _user:
        raise HTTPException(status_code=400, detail="User already exists.")

    new_user = User(**user.model_dump())  

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user