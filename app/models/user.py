# app/models/users.py

from pydantic import BaseModel, Field
from fastapi import Form

from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., description="The username of the user")
    email: str = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user")
    
class UserCreate(UserBase):
    user_level_id: int = Field(..., description="The user level ID of the user")    
    pass

class User(UserCreate):
    user_id: int = Field(..., description="The unique ID of the user")

    class Config:
        from_attributes = True        
        
