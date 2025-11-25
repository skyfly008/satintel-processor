from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from ..models.schema import TaskRequest, TaskResponse, BatchRequest
from ..services import analysis

router = APIRouter()


@router.post("/task", response_model=TaskResponse)
async def api_task(req: TaskRequest):
    res = await analysis.process_task(req)
    return res


@router.post("/batch_task", response_model=List[TaskResponse])
async def api_batch_task(req: BatchRequest, background_tasks: BackgroundTasks):
    # queue batch processing and return immediately
    background_tasks.add_task(analysis.process_batch, req)
    return [TaskResponse(task_id=str(i), status="queued") for i, _ in enumerate(req.tasks)]
