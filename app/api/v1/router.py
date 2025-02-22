from fastapi import APIRouter
from app.api.v1.endpoints import health, recieve_specs

api_router = APIRouter()
api_router.include_router(health.router)


api_router.include_router(recieve_specs.router)
