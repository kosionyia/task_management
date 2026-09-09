from contextlib import asynccontextmanager
from fastapi import  FastAPI
from db import create_db_and_tables, engine
from user.router import router as user_router
from task.router import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

    engine.dispose()
    print("Database connection closed.")

app = FastAPI(lifespan=lifespan)




app.include_router(user_router, tags=["User"])
app.include_router(task_router, tags=["Task"])