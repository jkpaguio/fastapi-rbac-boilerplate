# app/models/__init__.py
from sqlalchemy import Table, Column, Integer, String
from app.db import metadata  # Import the metadata instance from app/db.py

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(200)),
)

users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_level_id", Integer),
    Column("username", String(50)),
    Column("email", String(50)),
    Column("password", String(120)),
)

user_levels = Table(
    "user_levels",
    metadata,
    Column("user_level_id", Integer, primary_key=True),
    Column("user_level_name", String(50)),
)

user_level_permissions = Table(
    "user_level_permissions",
    metadata,
    Column("user_level_permission_id", Integer, primary_key=True),
    Column("user_level_id", Integer),
    Column("table_name", String(120)),
    Column("permission", Integer),
)