# FILE: app/api/v1/endpoints/temples.py
# (No changes here)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_main import temple as crud_temple
from app.schemas.all_schemas import Temple, TempleWithServices
router = APIRouter()
@router.get("/", response_model=List[Temple])
def read_temples(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    temples = crud_temple.get_multi(db, skip=skip, limit=limit)
    return temples
@router.get("/{temple_id}", response_model=TempleWithServices)
def read_temple(temple_id: int, db: Session = Depends(deps.get_db)):
    db_temple = crud_temple.get_with_services(db, id=temple_id)
    if db_temple is None:
        raise HTTPException(status_code=404, detail="Temple not found")
    return db_temple
