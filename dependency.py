import os
from typing_extensions import Annotated

from fastapi import Depends, HTTPException, Header
from pydantic import BaseModel

TASK_API_KEY = os.getenv("TASK_API_KEY")

if not TASK_API_KEY:
    raise RuntimeError("TASK_API_KEY is not configured")

def confirm_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != {TASK_API_KEY}:
        raise HTTPException(status_code=401, detail="Invalid API Key")

api_key_dependency = Depends(confirm_api_key)
        
class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 10
