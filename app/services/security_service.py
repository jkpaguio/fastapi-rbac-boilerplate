# app/services/security_service.py

from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import datetime, timedelta
from ..services import user_service

import jwt

import os

ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def create_access_token(data: dict, expires_delta: int):  
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta.total_seconds())
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRET'), algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    user = await user_service.get_user_by_username(username)
    if not user:
        return False
    try:
        if not verify_password(password, user.password):
            return False
    except UnknownHashError:
        return False
    return user