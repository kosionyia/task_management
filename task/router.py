from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlmodel import select
from datetime import datetime, timezone
from db import SessionDep
from task.log import log_completion_report
from task.model import Status, TaskCreate, TaskResponse
from task.schema import Task
from user.schema import User
from dependency import PaginationParams, api_key_dependency

router = APIRouter(prefix="/task", dependencies=[api_key_dependency])


@router.post("/", status_code=201, response_model=TaskResponse)
async def create_task(
    task: TaskCreate, session: SessionDep, user_id: Annotated[EmailStr, Query()]
):
    new_task = Task(**task.model_dump(), user_id=user_id)

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/", response_model=list[Task])
async def get_tasks(session: SessionDep, q: Annotated[PaginationParams, Depends()]):
    tasks = session.exec(select(Task).offset(q.skip).limit(q.limit)).all()
    return tasks


@router.put("/{task_id}", response_model=TaskCreate)
async def update_task(
    task_id: int, 
    task: TaskCreate, 
    session: SessionDep, 
    background_tasks: BackgroundTasks
    ):

    existing_task = session.get(Task, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    was_completed = existing_task.status == Status.DONE

    task_data = task.model_dump(exclude_unset=True)
    existing_task.sqlmodel_update(task_data)

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)

    # TODO: start background task to log completion time if status is completed to a file.

    if task.status == Status.DONE and not was_completed:
        assert existing_task.id is not None

        task_id_copy = existing_task.id
        title_copy = existing_task.title
        user_id_copy = existing_task.user_id
        completed_at_copy = datetime.now(timezone.utc)

        background_tasks.add_task(
            log_completion_report,
            task_id=task_id_copy,
            title=title_copy,
            user_id=user_id_copy,
            completed_at=completed_at_copy,
        )


    return existing_task


@router.patch("/{task_id}/status", response_model=TaskCreate)
async def update_task_status(
    task_id: int, status: Status, session: SessionDep, background_tasks: BackgroundTasks
):
    existing_task = session.get(Task, task_id)

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    was_completed = existing_task.status == Status.DONE
    existing_task.status = status

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)

    if status == Status.DONE and not was_completed:
        assert existing_task.id is not None

        task_id_copy = existing_task.id
        title_copy = existing_task.title
        user_id_copy = existing_task.user_id
        completed_at_copy = datetime.now(timezone.utc)

        background_tasks.add_task(
            log_completion_report,
            task_id=task_id_copy,
            title=title_copy,
            user_id=user_id_copy,
            completed_at=completed_at_copy,
        )

    return existing_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: SessionDep):
    existing_task = session.get(Task, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    session.delete(existing_task)
    session.commit()

    return {"message": "Task deleted successfully."}
