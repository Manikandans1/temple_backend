
# FILE: app/main.py
# !! THIS FILE IS CORRECTED !!
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api.v1.api import api_router
from app.core.config import settings
from app.db import session, base
from app.crud.crud_main import temple as crud_temple, user as crud_user
from app.schemas.all_schemas import TempleCreate, UserCreate
from app.models.all_models import UserRole

base.Base.metadata.create_all(bind=session.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_initial_data(db: Session):
    from app.models import all_models as models
    # Create Admin User if not exists
    if not db.query(models.User).filter(models.User.role == UserRole.admin).first():
        print("Creating initial admin user...")
        admin_user_in = UserCreate(
            phone_number="+919999999999", # Use a real number for testing
            name="Temple Admin",
            email="admin@temple.com"
        )
        admin_user = crud_user.create(db, obj_in=admin_user_in)
        admin_user.role = UserRole.admin
        db.commit()
        print("Admin user created with phone +919999999999")

    # Create Temples if not exists
    if not db.query(models.Temple).first():
        print("Creating initial temple data...")
        temple1_in = TempleCreate(name="Brihadeeswarar Temple", location="Thanjavur, Tamil Nadu", image_url="https://i.imgur.com/b1x23dF.jpg", description="An architectural marvel dedicated to Lord Shiva.")
        temple2_in = TempleCreate(name="Meenakshi Amman Temple", location="Madurai, Tamil Nadu", image_url="https://i.imgur.com/Jh2mGye.jpg", description="A historic Hindu temple on the southern bank of the Vaigai River.")
        
        temple1 = crud_temple.create(db, obj_in=temple1_in)
        temple2 = crud_temple.create(db, obj_in=temple2_in)
        
        pooja1 = models.PoojaService(name="Archana", description="A special pooja by chanting the name of the deity.", price=250.00, estimated_time="15 mins", temple_id=temple1.id)
        pooja2 = models.PoojaService(name="Abishekam", description="The sacred bathing ceremony of the deity.", price=750.00, estimated_time="45 mins", temple_id=temple1.id)
        pooja3 = models.PoojaService(name="Special Darshan", description="Quick darshan for devotees.", price=100.00, estimated_time="10 mins", temple_id=temple2.id)
        
        db.add_all([pooja1, pooja2, pooja3])
        db.commit()
        print("Initial data created.")

@app.on_event("startup")
def on_startup():
    db = session.SessionLocal()
    create_initial_data(db)
    db.close()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
