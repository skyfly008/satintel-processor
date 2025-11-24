from ..models.schema import TaskRequest, TaskResponse, BatchRequest
from typing import List
import asyncio


async def process_task(req: TaskRequest) -> TaskResponse:
    # placeholder orchestration: fetch imagery -> detect -> change detect -> package
    await asyncio.sleep(0.1)
    results = {"area_id": req.area_id, "date": req.date, "summary": "demo result"}
    return TaskResponse(task_id=req.task_id or f"{req.area_id}:{req.date}", status="done", results=results)


async def process_batch(req: BatchRequest) -> List[TaskResponse]:
    # naive concurrent processing for demo
    tasks = [process_task(t) for t in req.tasks]
    results = await asyncio.gather(*tasks)
    return results
