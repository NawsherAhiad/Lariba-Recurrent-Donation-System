from fastapi.middleware.cors import CORSMiddleware
from app.api.donation import router as donation_router
from app.api.bkash import router as bkash_router
from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for LARIBA Donation Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",   # Add this
        "http://localhost:5501",   # Optional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    donation_router,
    prefix="/api/v1",
    tags=["Donations"],
)

app.include_router(
    bkash_router,
    prefix="/api/v1",
    tags=["bKash"],
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }