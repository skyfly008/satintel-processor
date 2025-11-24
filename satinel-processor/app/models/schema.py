from pydantic import BaseModel
from typing import List, Optional


class TaskRequest(BaseModel):
    task_id: Optional[str] = None
    area_id: str
    date: str
    imagery_source: Optional[str] = None


class BatchRequest(BaseModel):
    tasks: List[TaskRequest]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[dict] = None
