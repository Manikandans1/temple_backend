# FILE: app/api/deps.py
# (No changes here)
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.all_models import User, UserRole
from app.schemas.all_schemas import TokenPayload
from app.crud.crud_main import user as crud_user


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/verify-otp")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM] # <-- CORRECTED: Uses settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user



# reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/verify-otp")

# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = db.query(User).filter(User.id == token_data.sub).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# # NEW: Dependency to get an admin user
# def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
#     if current_user.role != UserRole.admin:
#         raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
#     return current_user
