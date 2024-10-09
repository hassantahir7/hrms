# app/apis/auth/schemas.py

from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    job_title_id: UUID  # Change to UUID to match the foreign key reference
    joining_date: date
    professional_picture: Optional[str] = None  # URL or file path
    cnic_no: str
    date_of_birth: date
    qualification: str
    email: str
    contact_no: str
    address: str
    blood_group: str
    emergency_contact_details: str
    relation: str
    bank_detail: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: UUID  # Change id type to UUID
    username: str
    full_name: str
    job_title: Optional[str]  # Keep job_title as an optional string
    joining_date: date
    professional_picture: Optional[str] = None  # URL or file path
    cnic_no: str
    date_of_birth: date
    qualification: str
    email: str
    contact_no: str
    address: str
    blood_group: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserWithToken(BaseModel):
    user: UserOut
    token: str
