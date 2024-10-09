# app/apis/job_titles/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.apis.designation import schemas, services
from app.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=schemas.DesignationOut)
def create_designation(designation: schemas.DesignationCreate, db: Session = Depends(get_db)):
    return services.create_designation(db=db, designation=designation)

@router.get("/{designation_id}", response_model=schemas.DesignationOut)
def read_designation(designation_id: UUID, db: Session = Depends(get_db)):
    return services.get_designation(db=db, designation_id=designation_id)

@router.get("/", response_model=list[schemas.DesignationOut])
def read_designations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return services.get_designations(db=db, skip=skip, limit=limit)

@router.put("/{designation_id}", response_model=schemas.DesignationOut)
def update_designation(designation_id: UUID, designation: schemas.DesignationCreate, db: Session = Depends(get_db)):
    return services.update_designation(db=db, designation_id=designation_id, designation=designation)

@router.delete("/{designation_id}")
def delete_designation(designation_id: UUID, db: Session = Depends(get_db)):
    services.delete_designation(db=db, designation_id=designation_id)
    return {"message": "Designation deleted successfully."}
