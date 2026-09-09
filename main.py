from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import create_db_and_tables, engine, SessionDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

    engine.dispose()
    print("Database connection closed.")

app = FastAPI(lifespan=lifespan)