# app/routes/users.py

from fastapi import APIRouter, HTTPException, Form
from typing import Optional
from ..models.user import User, UserCreate, UserBase
from ..services import user_service, security_service
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import uuid

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"bearer": "Access to the API with a bearer token"}
)

@router.post("/register", response_model=User, summary="User Registration")
async def register_user(user: UserBase):
    if not user.username:
        raise HTTPException(status_code=422, detail="Username is required")
    if not user.email:
        raise HTTPException(status_code=422, detail="Email is required")
    if not user.password:
        raise HTTPException(status_code=422, detail="Password is required")    
    
    default_user_level_id = 1
    user_info = UserCreate(
        user_level_id=default_user_level_id,
        username=user.username,
        email=user.email,
        password=security_service.get_password_hash(user.password)
    )
    return await user_service.create_user(user_info)


@router.post("/login", operation_id="UserLogin")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    expire: Optional[int] = Form(3600)
):
    user = await security_service.authenticate_user(username, password)
    print ("USER INFO", user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(seconds=expire)
    payload = {
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "iss": "localhost",
        "nbf": datetime.utcnow(),
        "exp": datetime.utcnow() + access_token_expires,
        "values": {
            "username": user.username,
            "userid": user.user_id,
            "parentuserid": 0,
            "userlevel": user.user_level_id,
            "userprimarykey": user.user_id,
            "permission": False
        }
    }
    access_token = security_service.create_access_token(
        data=payload, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "expires_in": expire}
