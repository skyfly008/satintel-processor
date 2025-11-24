# Satinel Processor (scaffold)

This repository is a scaffold for a satellite imagery processing service with batch support.

- `app/` - FastAPI app with endpoints in `app/routers/satinel.py` including `/api/task` and `/api/batch_task`.
- `satinel/` - Core processing package (ML wrappers, fetch logic, change detection).
- `data/` - Static imagery, masks, overlays and `cache/` for dynamic fetches.
- `tests/` - Basic pytest tests.

Run locally (example):

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

This scaffold provides minimal stubs for development and testing; replace placeholder logic with production implementations as needed.
