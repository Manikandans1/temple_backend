# FILE: app/crud/crud_main.py
# !! THIS FILE IS CORRECTED !!
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from app.crud.crud_base import CRUDBase
from app.models import all_models as models
from app.schemas import all_schemas as schemas
from app.core.security import get_password_hash


# ... (CRUDUser and CRUDTemple are unchanged) ...
class CRUDUser(CRUDBase[models.User, schemas.UserCreate]):
    def get_by_phone(self, db: Session, *, phone_number: str):
        return db.query(self.model).filter(models.User.phone_number == phone_number).first()
    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(phone_number=obj_in.phone_number, name=obj_in.name, email=obj_in.email)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDTemple(CRUDBase[models.Temple, schemas.TempleCreate]):
    def get_with_services(self, db: Session, *, id: int):
        return db.query(self.model).options(joinedload(self.model.services)).filter(self.model.id == id).first()
    
    def update(self, db: Session, *, db_obj: models.Temple, obj_in: schemas.TempleUpdate) -> models.Temple:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
class CRUDPoojaService(CRUDBase[models.PoojaService, schemas.PoojaServiceCreate]):
    def create_for_temple(self, db: Session, *, obj_in: schemas.PoojaServiceCreate, temple_id: int):
        db_obj = models.PoojaService(**obj_in.model_dump(), temple_id=temple_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDPromoCode(CRUDBase[models.PromoCode, schemas.PromoCodeCreate]):
    def get_by_code(self, db: Session, *, code: str):
        return db.query(self.model).filter(models.PromoCode.code == code, models.PromoCode.is_active == True).first()


class CRUDBooking(CRUDBase[models.Booking, schemas.BookingCreate]):
    # THIS FUNCTION IS CORRECTED to be a single, reliable transaction
    def create_with_owner(self, db: Session, *, obj_in: schemas.BookingCreate, user_id: int):
        # 1. Create the main Booking object in memory
        db_booking = models.Booking(
            booking_date=obj_in.booking_date, total_amount=obj_in.total_amount,
            video_option=obj_in.video_option, devotee_name=obj_in.devotee_name,
            devotee_nakshatra=obj_in.devotee_nakshatra, user_id=user_id,
            temple_id=obj_in.temple_id, pooja_service_id=obj_in.pooja_id
        )
        db.add(db_booking)
        
        # 2. Flush the session to get the ID for the new booking without committing the transaction yet
        db.flush()

        # 3. Create the dependent FamilyMember and PoojaStage objects
        for member in obj_in.family_members:
            db.add(models.FamilyMember(name=member.name, nakshatra=member.nakshatra, booking_id=db_booking.id))
        
        initial_stages = [
            models.PoojaStage(title="Booking Confirmed", description="We have received your booking details.", status=models.StageStatus.completed, timestamp=datetime.now(timezone.utc), booking_id=db_booking.id),
            models.PoojaStage(title="Sankalpam Preparation", description="Your details are being prepared for the sankalpam.", status=models.StageStatus.pending, booking_id=db_booking.id),
            models.PoojaStage(title="Pooja in Progress", description="The priest is currently performing the pooja on your behalf.", status=models.StageStatus.pending, booking_id=db_booking.id),
            models.PoojaStage(title="Pooja Completed", description="Your pooja has been successfully completed by the priest.", status=models.StageStatus.pending, booking_id=db_booking.id),
        ]
        db.add_all(initial_stages)

        # 4. Commit the entire transaction at once
        db.commit()
        db.refresh(db_booking)
        return db_booking

    def get_multi_by_owner(self, db: Session, *, user_id: int):
        return db.query(self.model).filter(models.Booking.user_id == user_id).order_by(models.Booking.booking_date.desc()).all()
    def get_multi_by_temple(self, db: Session, *, temple_id: int):
        return db.query(self.model).filter(models.Booking.temple_id == temple_id).order_by(models.Booking.booking_date.desc()).all()
    def update_stage(self, db: Session, *, booking_id: int, stage_id: int, status: models.StageStatus):
        stage = db.query(models.PoojaStage).filter(models.PoojaStage.booking_id == booking_id, models.PoojaStage.id == stage_id).first()
        if stage:
            stage.status = status
            if status == models.StageStatus.completed or status == models.StageStatus.inProgress:
                stage.timestamp = datetime.now(timezone.utc)
            db.commit()
            db.refresh(stage)
            return stage
        return None

# --- NEW CLASS TO HANDLE POOJA SERVICES ---
class CRUDPoojaService(CRUDBase[models.PoojaService, schemas.PoojaServiceCreate]):
    def create_for_temple(self, db: Session, *, obj_in: schemas.PoojaServiceCreate, temple_id: int):
        # Creates a new service and links it to the correct temple
        db_obj = models.PoojaService(**obj_in.model_dump(), temple_id=temple_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user = CRUDUser(models.User)
temple = CRUDTemple(models.Temple)
pooja_service = CRUDPoojaService(models.PoojaService)
promo_code = CRUDPromoCode(models.PromoCode)
booking = CRUDBooking(models.Booking)
