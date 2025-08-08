# NEW FILE: app/api/v1/endpoints/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_main as crud
from app.models import all_models as models
from app.schemas import all_schemas as schemas

router = APIRouter()

@router.get("/bookings/temple/{temple_id}", response_model=List[schemas.Booking])
def get_temple_bookings(
    temple_id: int,
    db: Session = Depends(deps.get_db),
    admin_user: models.User = Depends(deps.get_current_admin_user)
):
    bookings = crud.booking.get_multi_by_temple(db, temple_id=temple_id)
    return [
        { "id": b.id, "temple_name": b.temple.name, "temple_image_url": b.temple.image_url,
          "pooja_name": b.pooja_service.name, "booking_date": b.booking_date,
          "price": b.pooja_service.price, "status": b.status, "stages": b.stages, }
        for b in bookings
    ]

@router.put("/bookings/stage", response_model=schemas.PoojaStage)
def update_booking_stage(
    update_data: schemas.BookingStageUpdate,
    db: Session = Depends(deps.get_db),
    admin_user: models.User = Depends(deps.get_current_admin_user)
):
    updated_stage = crud.booking.update_stage(
        db, booking_id=update_data.booking_id, stage_id=update_data.stage_id, status=update_data.status
    )
    if not updated_stage:
        raise HTTPException(status_code=404, detail="Stage or Booking not found")
    return updated_stage

# You would add endpoints for creating temples, services, promos here following a similar pattern.

# --- Temple & Service Management ---
@router.post("/temples", response_model=schemas.Temple)
def create_temple(temple_in: schemas.TempleCreate, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    return crud.temple.create(db, obj_in=temple_in)

@router.post("/temples/{temple_id}/services", response_model=schemas.PoojaService)
def create_pooja_service_for_temple(temple_id: int, service_in: schemas.PoojaServiceCreate, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    return crud.pooja_service.create_for_temple(db, obj_in=service_in, temple_id=temple_id)

@router.delete("/temples/{temple_id}", response_model=schemas.Temple) # <-- NEW
def delete_temple(temple_id: int, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    deleted_temple = crud.temple.remove(db, id=temple_id)
    if not deleted_temple:
        raise HTTPException(status_code=404, detail="Temple not found")
    return deleted_temple

@router.put("/temples/{temple_id}", response_model=schemas.Temple)
def update_temple(
    temple_id: int,
    temple_in: schemas.TempleUpdate,
    db: Session = Depends(deps.get_db),
    admin_user: models.User = Depends(deps.get_current_admin_user)
):
    db_temple = crud.temple.get(db, id=temple_id)
    if not db_temple:
        raise HTTPException(status_code=404, detail="Temple not found")
    return crud.temple.update(db, db_obj=db_temple, obj_in=temple_in)


# --- Promo Code Management ---
@router.post("/promos", response_model=schemas.PromoCode)
def create_promo_code(promo_in: schemas.PromoCodeCreate, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    promo_in.code = promo_in.code.upper()
    return crud.promo_code.create(db, obj_in=promo_in)

@router.get("/promos", response_model=List[schemas.PromoCode]) # <-- NEW
def get_promo_codes(db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    return crud.promo_code.get_multi(db)

@router.delete("/promos/{promo_id}", response_model=schemas.PromoCode) # <-- NEW
def delete_promo_code(promo_id: int, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    deleted_promo = crud.promo_code.remove(db, id=promo_id)
    if not deleted_promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return deleted_promo



# --- Booking Management ---
@router.get("/bookings/temple/{temple_id}", response_model=List[schemas.Booking])
def get_temple_bookings(temple_id: int, db: Session = Depends(deps.get_db), admin_user: models.User = Depends(deps.get_current_admin_user)):
    bookings = crud.booking.get_multi_by_temple(db, temple_id=temple_id)
    return [{"id": b.id, "temple_name": b.temple.name, "temple_image_url": b.temple.image_url, "pooja_name": b.pooja_service.name, "booking_date": b.booking_date, "price": b.pooja_service.price, "status": b.status, "stages": b.stages} for b in bookings]

@router.put("/bookings/{booking_id}/stages/{stage_id}", response_model=schemas.PoojaStage) # <-- UPDATED PATH
def update_booking_stage(
    booking_id: int, stage_id: int, update_data: schemas.BookingStageUpdate,
    db: Session = Depends(deps.get_db),
    admin_user: models.User = Depends(deps.get_current_admin_user)
):
    updated_stage = crud.booking.update_stage(db, booking_id=booking_id, stage_id=stage_id, status=update_data.status)
    if not updated_stage:
        raise HTTPException(status_code=404, detail="Stage or Booking not found")
    return updated_stage

# --- NEW ENDPOINT TO ADD A SERVICE ---
@router.post("/temples/{temple_id}/services", response_model=schemas.PoojaService)
def create_pooja_service_for_temple(
    temple_id: int,
    service_in: schemas.PoojaServiceCreate,
    db: Session = Depends(deps.get_db),
    admin_user: models.User = Depends(deps.get_current_admin_user)
):
    """
    Create a new pooja service for a specific temple.
    """
    return crud.pooja_service.create_for_temple(db, obj_in=service_in, temple_id=temple_id)
# --- END OF NEW ENDPOINT ---
