from fastapi import HTTPException, APIRouter # type: ignore[reportMissingImports]
from typing import List  # Add this for response model
from .database import get_db  # pyright: ignore[reportMissingImports]
from .schemas import UserCreate, UserResponse  # pyright: ignore[reportMissingImports]
from . import crud  # pyright: ignore[reportMissingImports]

router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    with get_db() as db:
        # Check if user with this email already exists
        existing_user = crud.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = crud.create_user(db, user)
        return UserResponse.model_validate(db_user)

@router.get("/list", response_model=List[UserResponse])
async def get_users():
    with get_db() as db:
        users = crud.get_users(db)
        return [UserResponse.model_validate(user) for user in users]

@router.get("/list/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    with get_db() as db:
        user = crud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

@router.put("/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    with get_db() as db:
        db_user = crud.update_user(db, user_id, user)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(db_user)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    with get_db() as db:
        success = crud.delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}