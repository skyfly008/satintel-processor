from app.services import analysis
from app.models.schema import TaskRequest
import asyncio


def test_process_task():
    req = TaskRequest(area_id="AREA_1", date="2023-01-01")
    res = asyncio.get_event_loop().run_until_complete(analysis.process_task(req))
    assert res.status == "done"


def test_process_batch():
    req = TaskRequest(area_id="AREA_1", date="2023-01-01")
    from app.models.schema import BatchRequest
    br = BatchRequest(tasks=[req, req])
    results = asyncio.get_event_loop().run_until_complete(analysis.process_batch(br))
    assert len(results) == 2
