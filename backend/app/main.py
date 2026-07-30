from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.donation import router as donation_router
from app.api.bkash import router as bkash_router
from app.api.health import router as health_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for LARIBA Donation Platform",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routers
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    donation_router,
    prefix="/api/v1",
    tags=["Donations"]
)

app.include_router(
    bkash_router,
    prefix="/api/v1",
    tags=["bKash"]
)


# Frontend directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# Serve donation page at root
@app.get("/")
async def serve_root():
    return FileResponse(
        FRONTEND_DIR / "donation.html"
    )


# Serve frontend files:
# /frontend/thankyou.html
# /frontend/style.css
# /frontend/script.js
if FRONTEND_DIR.exists():
    app.mount(
        "/frontend",
        StaticFiles(directory=str(FRONTEND_DIR)),
        name="frontend"
    )