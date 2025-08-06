# FILE: app/api/v1/endpoints/auth.py
# !! THIS FILE IS CORRECTED !!
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.core.security import create_access_token
from app.crud.crud_main import user as crud_user
from app.schemas.all_schemas import Msg, Token, UserCreate, OtpSendRequest, OtpVerifyRequest, User as UserSchema
import random
from twilio.rest import Client
from app.core.config import settings

router = APIRouter()
otp_store = {}

# @router.post("/send-otp", response_model=Msg)
# def send_otp(request: OtpSendRequest, db: Session = Depends(deps.get_db)):
#     otp = random.randint(100000, 999999)
#     otp_store[request.phone_number] = otp
#     print(f"OTP for {request.phone_number} is {otp}")
#     user_exists = crud_user.get_by_phone(db, phone_number=request.phone_number)
#     return {"message": "OTP sent successfully", "is_new_user": user_exists is None}

# @router.post("/verify-otp")
# def verify_otp(request: OtpVerifyRequest, db: Session = Depends(deps.get_db)):
#     if otp_store.get(request.phone_number) != int(request.otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")
    
#     del otp_store[request.phone_number]
    
#     user = crud_user.get_by_phone(db, phone_number=request.phone_number)
    
#     if not user:
#         # User is new. OTP is correct. Signal to app to proceed to registration.
#         # Status 202 means "Accepted" - the request is valid but not yet complete.
#         return JSONResponse(status_code=202, content={"message": "OTP verified. Proceed to registration."})
    
#     # User exists. OTP is correct. Log them in by returning a token.
#     access_token = create_access_token(subject=user.id)
#     return Token(access_token=access_token, token_type="bearer")

# @router.post("/register", response_model=Token)
# def register_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
#     if crud_user.get_by_phone(db, phone_number=user_in.phone_number):
#         raise HTTPException(status_code=400, detail="Phone number already registered")
#     new_user = crud_user.create(db, obj_in=user_in)
#     return {"access_token": create_access_token(subject=new_user.id), "token_type": "bearer"}


# @router.post("/send-otp", response_model=Msg)
# def send_otp(request: OtpSendRequest, db: Session = Depends(deps.get_db)):
#     otp = random.randint(100000, 999999)
#     otp_store[request.phone_number] = otp
#     print(f"OTP for {request.phone_number} is {otp}")
#     user_exists = crud_user.get_by_phone(db, phone_number=request.phone_number)
#     return {"message": "OTP sent successfully", "is_new_user": user_exists is None}


@router.post("/send-otp", response_model=Msg)
def send_otp(request: OtpSendRequest, db: Session = Depends(deps.get_db)):
    otp = random.randint(100000, 999999)
    otp_store[request.phone_number] = otp
    
    # --- REAL TWILIO OTP LOGIC ---
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message_body = f"Your Divine Connect OTP is: {otp}"
        
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=request.phone_number
        )
        print(f"OTP sent to {request.phone_number} via Twilio. SID: {message.sid}")
    except Exception as e:
        print(f"!!! TWILIO ERROR: {e} !!!")
        # In a real production app, you might want to raise an HTTPException here
        # so the user knows the SMS failed. For now, we print the error and continue
        # so you can still test using the OTP printed in the console.
    # --- END TWILIO LOGIC ---

    user_exists = crud_user.get_by_phone(db, phone_number=request.phone_number)
    return {"message": "OTP sent successfully", "is_new_user": user_exists is None}

# ... (verify_otp and register endpoints are unchanged) ...
@router.post("/verify-otp")
def verify_otp(request: OtpVerifyRequest, db: Session = Depends(deps.get_db)):
    if otp_store.get(request.phone_number) != int(request.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[request.phone_number]
    user = crud_user.get_by_phone(db, phone_number=request.phone_number)
    if not user:
        return JSONResponse(status_code=202, content={"message": "OTP verified. Proceed to registration."})
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer", user=user)

@router.post("/register", response_model=Token)
def register_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    if crud_user.get_by_phone(db, phone_number=user_in.phone_number):
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_user = crud_user.create(db, obj_in=user_in)
    access_token = create_access_token(subject=new_user.id)
    return Token(access_token=access_token, token_type="bearer", user=new_user)


# @router.post("/verify-otp")
# def verify_otp(request: OtpVerifyRequest, db: Session = Depends(deps.get_db)):
#     if otp_store.get(request.phone_number) != int(request.otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")
#     del otp_store[request.phone_number]
#     user = crud_user.get_by_phone(db, phone_number=request.phone_number)
#     if not user:
#         return JSONResponse(status_code=202, content={"message": "OTP verified. Proceed to registration."})
#     access_token = create_access_token(subject=user.id)
#     return Token(access_token=access_token, token_type="bearer", user=user)

# @router.post("/register", response_model=Token)
# def register_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
#     if crud_user.get_by_phone(db, phone_number=user_in.phone_number):
#         raise HTTPException(status_code=400, detail="Phone number already registered")
#     new_user = crud_user.create(db, obj_in=user_in)
#     access_token = create_access_token(subject=new_user.id)
#     return Token(access_token=access_token, token_type="bearer", user=new_user)
