import time

from fastapi import APIRouter

from src.presentation.http.system.dtos.health import HealthResponse

router = APIRouter(prefix="/system", tags=["System"])

_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", uptime=str(time.time() - _start_time))
