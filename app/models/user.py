from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum

class UserRole(enum.Enum):
    admin = "admin"
    dev = "dev"
    user = "user"

class User(BaseModel):
    user_id: Optional[str] = None
    username: str
    email: str
    hashed_password: str
    role: UserRole = UserRole.user
    is_active: bool = True
    create_at: Optional[str] = None
    update_at: Optional[str] = None 