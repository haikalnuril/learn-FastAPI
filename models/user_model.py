from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel) :
    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="User's username"
    )
    email: EmailStr = Field(
        description="User's email"
    )

class CreateUserRequest(UserResponse) :
    password: str = Field(
        ..., 
        min_length=8, 
        description="User's password (will be hashed)"
    )

class toUserResponse(UserResponse):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes= True