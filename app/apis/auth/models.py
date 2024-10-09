# app/apis/auth/models.py

import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID  # Use UUID for PostgreSQL
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Change to UUID
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    joining_date = Column(Date)
    professional_picture = Column(String)  # Assuming this is a URL or file path
    cnic_no = Column(String)
    date_of_birth = Column(Date)
    qualification = Column(String)
    email = Column(String, unique=True)
    contact_no = Column(String)
    address = Column(String)
    blood_group = Column(String)
    emergency_contact_details = Column(String)
    relation = Column(String)
    bank_detail = Column(String)

    job_title_id = Column(UUID, ForeignKey('designation.id'), nullable=True)

    job_title = relationship("Designation", back_populates="users")

