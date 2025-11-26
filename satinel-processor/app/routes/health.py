"""
Health Check Routes - Service health and status endpoints.
"""

from fastapi import APIRouter
from app.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check service health and availability.
    
    Returns:
        Service status and metadata
    """
    # TODO: Implement health check logic
    # - Check if data directories exist
    # - Count available areas
    # - Verify model availability
    
    return {
        "status": "healthy",
        "version": "0.1.0",
        "areas_available": 0
    }


@router.get("/areas")
async def list_areas():
    """
    List all available areas with imagery.
    
    Returns:
        List of area information
    """
    # TODO: Implement area listing
    # - Scan data/imagery/ directory
    # - Return area metadata
    pass
