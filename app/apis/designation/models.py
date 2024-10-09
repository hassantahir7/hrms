# app/apis/job_titles/models.py
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID  # Use UUID for PostgreSQL


class Designation(Base):
    __tablename__ = "designation"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)

    # Establish relationship with User
    users = relationship("User", back_populates="job_title")
