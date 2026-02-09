from fastapi import HTTPException, APIRouter # type: ignore[reportMissingImports]
from .schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from .database import get_db
from . import crud
from .helper import exception_helper

router = APIRouter()

@router.post("/create", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user with hashed password."""
    with get_db() as db:
        # Check if email already exists
        existing_user = crud.get_user_by_email(db, user.email)
        await exception_helper(user, "create", existing_user)
        
        # Create user (password will be hashed in crud.create_user)
        db_user = crud.create_user(db, user)
        return db_user

@router.post("/login")
async def login(credentials: UserLogin):
    """
    Authenticate a user.
    
    This verifies the email and password, checking the hashed password.
    """
    with get_db() as db:
        user = crud.authenticate_user(db, credentials.email, credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }

@router.get("/list", response_model=list[UserResponse])
async def get_users(skip: int = 0, limit: int = 100):
    """Get all users (passwords not included in response)."""
    with get_db() as db:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users

@router.get("/list/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a specific user (password not included in response)."""
    with get_db() as db:
        user = crud.get_user_by_id(db, user_id)
        await exception_helper(user, "get_id")
        return user

@router.put("/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    """Update a user (password will be re-hashed)."""
    with get_db() as db:
        db_user = crud.get_user_by_id(db, user_id)
        await exception_helper(db_user, "get_id")
        
        updated_user = crud.update_user(db, user_id, user)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Failed to update user")
        return updated_user

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    """Delete a user."""
    with get_db() as db:
        db_user = crud.get_user_by_id(db, user_id)
        await exception_helper(db_user, "get_id")
        
        success = crud.delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        return {"detail": "User deleted successfully"}