# app/apis/auth/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.apis.auth import schemas, services
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserWithToken)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return services.AuthService.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=schemas.UserWithToken)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        return services.AuthService.login_user(db=db, username=user.username, password=user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
