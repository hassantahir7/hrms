# app/apis/auth/services.py

import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from app.apis.auth import models, schemas
from app.apis.designation.models import Designation  # Import the Designation model

# Load environment variables from .env file
load_dotenv()

# Use environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a hashed password against a plain password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> schemas.UserWithToken:
        """Create a new user and return the user object and JWT token."""
        hashed_password = AuthService.hash_password(user.password)

        db_user = models.User(
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            joining_date=user.joining_date,
            professional_picture=user.professional_picture,
            cnic_no=user.cnic_no,
            date_of_birth=user.date_of_birth,
            qualification=user.qualification,
            email=user.email,
            contact_no=user.contact_no,
            address=user.address,
            blood_group=user.blood_group,
            emergency_contact_details=user.emergency_contact_details,
            relation=user.relation,
            bank_detail=user.bank_detail,
            job_title_id=user.job_title_id
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Fetch the job title
        job_title = db.query(Designation).filter(Designation.id == user.job_title_id).first()

        # Generate token
        token = AuthService.create_access_token(data={"sub": str(db_user.id)})

        # Manually construct UserOut
        user_out = schemas.UserOut(
            id=db_user.id,
            username=db_user.username,
            job_title=job_title.title if job_title else None  # Ensure job title is a string
        )

        return schemas.UserWithToken(user=user_out, token=token)

    @staticmethod
    def login_user(db: Session, username: str, password: str) -> schemas.UserWithToken:
        """Authenticate a user and return the user object and JWT token."""
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")

        # Fetch the job title
        job_title = db.query(Designation).filter(Designation.id == user.job_title_id).first()

        # Generate token
        token = AuthService.create_access_token(data={"sub": str(user.id)})

        # Manually construct UserOut
        user_out = schemas.UserOut(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            joining_date=user.joining_date,
            professional_picture=user.professional_picture,  # URL or file path
            cnic_no=user.cnic_no,
            date_of_birth=user.date_of_birth,
            qualification=user.qualification,
            email=user.email,
            contact_no=user.contact_no,
            address=user.address,
            blood_group=user.blood_group,
            job_title=job_title.title if job_title else None  # Ensure job title is a string
        )

        return schemas.UserWithToken(user=user_out, token=token)
