from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from ..models.schema import TaskRequest, TaskResponse, BatchRequest, BatchResponse
from ..services import analysis

router = APIRouter()


@router.post("/task", response_model=TaskResponse)
async def api_task(req: TaskRequest):
    res = await analysis.process_task(req)
    return res


@router.post("/batch_task", response_model=BatchResponse)
async def api_batch_task(req: BatchRequest):
    """Execute batch analysis with parallel processing and aggregated results."""
    result = await analysis.process_batch(req)
    return result
