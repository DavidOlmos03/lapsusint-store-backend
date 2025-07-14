from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas.user import User, UserCreate
from app.crud.user import user_crud
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token"""
    user = await user_crud.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["user_id"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@router.post("/register")
async def register(user_in: UserCreate):
    """Register a new user"""
    # Check if username already exists
    existing_user = await user_crud.get_by_username(user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await user_crud.get_by_email(user_in.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_data = await user_crud.create(user_in)
    return {
        "message": "User created successfully",
        "user": {
            "user_id": user_data["user_id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        }
    } 