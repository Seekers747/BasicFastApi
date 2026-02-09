from sqlalchemy.orm import Session # type: ignore[reportMissingImports]
from typing import Optional
from .models import User
from .schemas import UserCreate, UserUpdate
from .security import hash_password

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with hashed password."""
    # Hash the password before storing
    hashed_password = hash_password(user.password)
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password  # Store hashed password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """Update a user with hashed password."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        # Hash the password before updating
        db_user.password = hash_password(user.password)
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

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.
    
    Args:
        db: Database session
        username: User username
        password: Plain text password
    
    Returns:
        User object if authentication successful, None otherwise
    """
    from .security import verify_password
    
    user = get_user_by_username(db, username)
    if not user:
        return None
    
    # Verify the password
    if not verify_password(password, user.password):
        return None
    
    return user