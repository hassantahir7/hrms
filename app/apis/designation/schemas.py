# app/apis/job_titles/schemas.py

from pydantic import BaseModel
from uuid import UUID

class DesignationBase(BaseModel):
    title: str

class DesignationCreate(DesignationBase):
    pass

class DesignationOut(DesignationBase):
    id: UUID

    class Config:
        orm_mode = True
