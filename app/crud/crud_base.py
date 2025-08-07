# FILE: app/crud/crud_base.py
# (No changes here)
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# class CRUDBase(Generic[ModelType, CreateSchemaType]):
#     def __init__(self, model: Type[ModelType]):
#         self.model = model
#     def get(self, db: Session, id: Any) -> Optional[ModelType]:
#         return db.query(self.model).filter(self.model.id == id).first()
#     def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
#         return db.query(self.model).offset(skip).limit(limit).all()
#     def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
#         obj_in_data = obj_in.model_dump()
#         db_obj = self.model(**obj_in_data)
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # --- NEW DELETE FUNCTION ---
    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    # --- END OF NEW FUNCTION ---

