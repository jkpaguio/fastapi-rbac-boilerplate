# app/services/user_service.py

from ..models import users
from ..models.user import UserCreate
from ..db import database

async def create_user(user: UserCreate):
    query = users.insert().values(
        user_level_id = user.user_level_id, 
        username=user.username, 
        email=user.email, 
        password=user.password
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "user_id": last_record_id}

async def get_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

