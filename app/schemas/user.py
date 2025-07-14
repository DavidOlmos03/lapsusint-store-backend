from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    dev = "dev"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.user
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    user_id: str
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass 