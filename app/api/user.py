from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud.user import user_crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    """Get all users with pagination"""
    users = await user_crud.get_multi(skip=skip, limit=limit)
    return [User(**user) for user in users]

@router.post("/", response_model=User)
async def create_user(user_in: UserCreate):
    """Create a new user"""
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
    return User(**user_data)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    """Get a specific user by ID"""
    user_data = await user_crud.get(user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return User(**user_data)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_in: UserUpdate):
    """Update a user"""
    # Check if user exists
    existing_user = await user_crud.get(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if new username conflicts with existing user
    if user_in.username and user_in.username != existing_user["username"]:
        conflict_user = await user_crud.get_by_username(user_in.username)
        if conflict_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Check if new email conflicts with existing user
    if user_in.email and user_in.email != existing_user["email"]:
        conflict_email = await user_crud.get_by_email(user_in.email)
        if conflict_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user_data = await user_crud.update(user_id, user_in)
    return User(**user_data)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    success = await user_crud.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"} 