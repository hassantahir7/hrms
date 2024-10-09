from fastapi import FastAPI, HTTPException
from app.apis.auth import routes as auth_routes
from app.apis.designation import  routes as designation_routes
from dotenv import load_dotenv
import os

load_dotenv()


from app.database import engine, Base

# Create FastAPI app instance
app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Include routers for different modules
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(designation_routes.router, prefix="/designation", tags=["Designation"])
