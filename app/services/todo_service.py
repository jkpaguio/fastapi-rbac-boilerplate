# app/services/todo_service.py
from ..models import todos
from ..models.todo import TodoBase
from ..db import database
from sqlalchemy import delete, update

async def create_todo(todo: TodoBase):
    query = todos.insert().values(title=todo.title, description=todo.description)
    last_record_id = await database.execute(query)
    return {**todo.model_dump(), "id": last_record_id}

async def get_todo(id: int):
    query = todos.select().where(id == todos.c.id)
    return await database.fetch_one(query)

async def get_all_todos():
    query = todos.select()
    return await database.fetch_all(query)

async def delete_todo(id: int):
    query = delete(todos).where(todos.c.id == id)
    await database.execute(query)

async def update_todo(id: int, todo: TodoBase):
    query = (
        update(todos)
        .where(todos.c.id == id)
        .values(title=todo.title, description=todo.description)
    )
    await database.execute(query)