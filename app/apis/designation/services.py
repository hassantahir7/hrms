from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.apis.designation import models, schemas
from uuid import UUID
from fastapi import HTTPException

def create_designation(db: Session, designation: schemas.DesignationCreate) -> models.Designation:
    db_designation = models.Designation(**designation.model_dump())
    db.add(db_designation)
    try:
        db.commit()
        db.refresh(db_designation)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Designation already exists")
    return db_designation

def get_designation(db: Session, designation_id: UUID) -> models.Designation:
    db_designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not db_designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation

def get_designations(db: Session, skip: int = 0, limit: int = 10) -> list[models.Designation]:
    return db.query(models.Designation).offset(skip).limit(limit).all()

def update_designation(db: Session, designation_id: UUID, designation: schemas.DesignationCreate) -> models.Designation:
    db_designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not db_designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    for key, value in designation.dict().items():
        setattr(db_designation, key, value)
    db.commit()
    db.refresh(db_designation)
    return db_designation

def delete_designation(db: Session, designation_id: UUID):
    db_designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not db_designation:
        raise HTTPException(status_code=404, detail="Designation not found")

    db.delete(db_designation)
    db.commit()
