# --- App Configuration ---
# FILE: app/core/config.py
# (No changes here)
import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    PROJECT_NAME: str = "Divine Connect API"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    ALGORITHM = "HS256"
    # --- ADD THESE THREE LINES ---
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER")
settings = Settings()

