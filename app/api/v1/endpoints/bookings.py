# FILE: app/api/v1/endpoints/bookings.py
# (No changes here)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_main import booking as crud_booking, promo_code as crud_promo
from app.models.all_models import User
from app.schemas.all_schemas import Booking, BookingCreate, PromoResponse, PromoRequest


router = APIRouter()
@router.post("/create-detailed", response_model=Booking)
def create_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_in: BookingCreate,
    current_user: User = Depends(deps.get_current_user),
):
    booking = crud_booking.create_with_owner(db=db, obj_in=booking_in, user_id=current_user.id)
    response_booking = {
        "id": booking.id,
        "temple_name": booking.temple.name,
        "temple_image_url": booking.temple.image_url,
        "pooja_name": booking.pooja_service.name,
        "booking_date": booking.booking_date,
        "price": booking.pooja_service.price,
        "status": booking.status,
        "stages": booking.stages,
    }
    return response_booking
@router.get("/my-bookings", response_model=List[Booking])
def read_my_bookings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    bookings = crud_booking.get_multi_by_owner(db, user_id=current_user.id)
    response_bookings = []
    for booking in bookings:
        response_booking = {
            "id": booking.id,
            "temple_name": booking.temple.name,
            "temple_image_url": booking.temple.image_url,
            "pooja_name": booking.pooja_service.name,
            "booking_date": booking.booking_date,
            "price": booking.pooja_service.price,
            "status": booking.status,
            "stages": booking.stages,
        }
        response_bookings.append(response_booking)
    return response_bookings

# @router.post("/promos/validate", response_model=PromoResponse)
# def validate_promo(code: str):
#     if code.upper() == "DIVINE10":
#         return {"discount_value": 0.10, "message": "10% discount applied!"}
#     if code.upper() == "FESTIVAL50":
#         return {"discount_value": 50.0, "message": "Flat ₹50 discount applied!"}
#     raise HTTPException(status_code=404, detail="Invalid promo code")

@router.post("/promos/validate", response_model=PromoResponse)
def validate_promo(request: PromoRequest, db: Session = Depends(deps.get_db)):
    db_promo = crud_promo.get_by_code(db, code=request.code.upper())
    if not db_promo:
        raise HTTPException(status_code=404, detail="Invalid or expired promo code")
    
    discount = db_promo.discount_value
    message = f"Flat ₹{discount} discount applied!"
    if db_promo.is_percentage:
        message = f"{int(discount * 100)}% discount applied!"

    return {"discount_value": discount, "message": message}