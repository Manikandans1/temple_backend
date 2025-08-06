# FILE: app/models/all_models.py
# (No changes here)
import enum
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship
from app.db.base import Base



class UserRole(str, enum.Enum):
    admin = "admin"
    devotee = "devotee"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean(), default=True)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.devotee) # <-- ADDED ROLE

class Temple(Base):
    __tablename__ = "temples"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    services = relationship("PoojaService", back_populates="temple", cascade="all, delete-orphan")


class PoojaService(Base):
    __tablename__ = "pooja_services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    estimated_time = Column(String)
    temple_id = Column(Integer, ForeignKey("temples.id"))
    temple = relationship("Temple", back_populates="services")
class BookingStatus(str, enum.Enum):
    upcoming = "upcoming"
    completed = "completed"
    cancelled = "cancelled"
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(BookingStatus), nullable=False, default=BookingStatus.upcoming)
    total_amount = Column(Float, nullable=False)
    video_option = Column(String, nullable=True)
    devotee_name = Column(String)
    devotee_nakshatra = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    temple_id = Column(Integer, ForeignKey("temples.id"))
    pooja_service_id = Column(Integer, ForeignKey("pooja_services.id"))
    user = relationship("User")
    temple = relationship("Temple")
    pooja_service = relationship("PoojaService")
    family_members = relationship("FamilyMember", back_populates="booking")
    stages = relationship("PoojaStage", back_populates="booking")
class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nakshatra = Column(String, nullable=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    booking = relationship("Booking", back_populates="family_members")
class StageStatus(str, enum.Enum):
    completed = "completed"
    inProgress = "inProgress"
    pending = "pending"
class PoojaStage(Base):
    __tablename__ = "pooja_stages"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(StageStatus), nullable=False)
    timestamp = Column(DateTime, nullable=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    booking = relationship("Booking", back_populates="stages")

# NEW MODEL for Promo Codes
class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    discount_value = Column(Float, nullable=False) # e.g., 50.0 or 0.10
    is_percentage = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
