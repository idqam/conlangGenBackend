from fastapi import FastAPI
from .api.v1.router import api_router
from .core.config import settings
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
