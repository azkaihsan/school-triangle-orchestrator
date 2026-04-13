from fastapi import APIRouter
from ..schemas import HealthResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse, tags=["health"])
async def health_check():
    return HealthResponse(status="healthy")
