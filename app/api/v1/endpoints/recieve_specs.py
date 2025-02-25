from fastapi import APIRouter

from app.models.schemas import PayloadSpec




router = APIRouter()

@router.post("/submit-specs", summary="Gets lang specs from frontend")
async def process_language(payload: PayloadSpec ):
    
    return {"message": "Payload received lmao", "data": payload.model_dump()}
