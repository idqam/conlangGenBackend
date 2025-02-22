
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health Check", tags=["Health"])
async def health_check():
    return {"status": "ok"}
