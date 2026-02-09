from sqlalchemy.orm import Session # type: ignore[reportMissingImports]
from typing import Optional
from .models import User  # pyright: ignore[reportMissingImports]
from .schemas import UserCreate, UserUpdate  # pyright: ignore[reportMissingImports]

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password  # In production: hash this!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """Update a user."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password  # In production: hash this!
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False