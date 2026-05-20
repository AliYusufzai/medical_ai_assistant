from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username, 3-50 characters")
    email: EmailStr
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char in "!@#$%^&*" for char in value):
            raise ValueError("Password must contain at least one special character (!@#$%^&*)")
        return value
    
class UserResponse(UserBase):

    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserPublicResponse(BaseModel):


    id: int
    username: str

    model_config = {"from_attributes": True}

