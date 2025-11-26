"""
FastAPI Backend - Main application entry point.

Responsibilities:
- Initialize FastAPI app
- Configure CORS, static files, templates
- Mount API routes
- Serve main map UI
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Import routes
from app.routes import task, health

# Initialize FastAPI app
app = FastAPI(
    title="ASIP - Automated Satellite Intelligence Processor",
    description="Real-time satellite imagery analysis with AI-powered building detection",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(task.router, prefix="/api", tags=["tasking"])

# Root route - serves main map interface
@app.get("/")
async def root():
    """Serve main application UI."""
    # TODO: Return template with map interface
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
