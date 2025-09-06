# FILE: app/schemas/all_schemas.py
# !! THIS FILE IS CORRECTED !!
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.all_models import BookingStatus, StageStatus,  UserRole


class UserBase(BaseModel):
    phone_number: str = Field(..., pattern=r'^\+[1-9]\d{1,14}$')


class User(BaseModel): # <-- UPDATED to include role
    id: int
    phone_number: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: UserRole
    class Config: from_attributes = True

class Token(BaseModel): # <-- UPDATED to include user info on login
    access_token: str
    token_type: str
    user: User

class UserCreate(UserBase):
    name: str
    email: EmailStr

class TokenPayload(BaseModel):
    sub: Optional[int] = None
class Msg(BaseModel):
    message: str
    is_new_user: Optional[bool] = None

class OtpSendRequest(BaseModel):
    phone_number: str
class OtpVerifyRequest(BaseModel):
    phone_number: str
    otp: str

class PoojaServiceCreate(BaseModel):
    name: str
    description: str
    price: float
    estimated_time: str

class PoojaService(BaseModel):
    id: int
    name: str
    description: str
    price: float
    estimated_time: str
    class Config: from_attributes = True

class TempleBase(BaseModel):
    name: str
    location: str
    image_url: str
    description: str
class TempleCreate(TempleBase):
    pass

class TempleUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

class Temple(TempleBase):
    id: int
    class Config: from_attributes = True
class TempleWithServices(Temple):
    services: List[PoojaService] = []

# class FamilyMemberCreate(BaseModel):
#     name: str
#     nakshatra: Optional[str] = None
# class BookingCreate(BaseModel):
#     pooja_id: int
#     temple_id: int
#     booking_date: datetime
#     devotee_name: str
#     devotee_nakshatra: str
#     family_members: List[FamilyMemberCreate]
#     video_option: Optional[str] = None
#     total_amount: float

class FamilyMemberCreate(BaseModel):
    name: str
    nakshatra: Optional[str] = None

class BookingCreate(BaseModel):
    pooja_id: int
    temple_id: int
    booking_date: datetime
    devotee_name: str
    devotee_nakshatra: str
    family_members: List[FamilyMemberCreate]
    video_option: Optional[str] = None
    total_amount: float
    
    # --- NEW FIELDS FOR SHIPPING ADDRESS ---
    shipping_address_line1: Optional[str] = None
    shipping_address_line2: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_pincode: Optional[str] = None
    shipping_country: Optional[str] = None
    # --- END OF NEW FIELDS ---


class PoojaStage(BaseModel):
    title: str
    description: str
    status: StageStatus
    timestamp: Optional[datetime] = None
    class Config: from_attributes = True
class Booking(BaseModel):
    id: int
    temple_name: str
    temple_image_url: str
    pooja_name: str
    booking_date: datetime
    price: float
    status: BookingStatus
    stages: List[PoojaStage] = []
    class Config: from_attributes = True

class PromoResponse(BaseModel):
    discount_value: float
    message: str


class PromoCodeCreate(BaseModel):
    code: str
    discount_value: float # e.g., 50.0 for flat discount, 0.10 for 10%
    is_percentage: bool

class BookingStageUpdate(BaseModel):
    stage_id: int
    status: StageStatus


# NEW SCHEMA for creating Promo Codes
class PromoCodeCreate(BaseModel):
    code: str
    discount_value: float
    is_percentage: bool

class PromoCode(PromoCodeCreate):
    id: int
    is_active: bool
    class Config: from_attributes = True

# ... (all other schemas are the same) ...

class PromoRequest(BaseModel): # <-- THIS CLASS WAS MISSING
    code: str

# ... (rest of the file is the same) ...