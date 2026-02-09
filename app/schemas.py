from pydantic import BaseModel, EmailStr, Field # type: ignore[reportMissingImports]

# Base schema with common attributes
class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")

# Schema for creating a user (includes password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

# Schema for updating a user
class UserUpdate(UserBase):
    password: str = Field(..., min_length=8, description="User password")

# Schema for returning user data (NO PASSWORD!)
class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str