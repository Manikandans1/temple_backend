# FILE: app/api/v1/api.py
# (No changes here)
from fastapi import APIRouter
from app.api.v1.endpoints import auth, temples, bookings, admin
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(temples.router, prefix="/temples", tags=["Temples & Poojas"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
