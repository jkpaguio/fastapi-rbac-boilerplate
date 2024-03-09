# app/routes/todos.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.todo import Todo, TodoCreate, TodoBase
from ..services import todo_service
from .security import get_oauth2_password_bearer
from ..lib.cache_it import cache_it_async
router = APIRouter()

@router.post("/", response_model=Todo, summary="Create a new todo")
async def create_todo(todo: TodoCreate, user_access: dict = Depends(get_oauth2_password_bearer)):
    print (user_access)
    return await todo_service.create_todo(todo)

@router.get("/{id}", response_model=Todo, summary="Get a todo by ID")
async def read_todo(id: int, user_access: dict = Depends(get_oauth2_password_bearer)):
    todo = await todo_service.get_todo(id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.get("/", response_model=List[Todo], summary="Get all todos")
@cache_it_async()
async def read_todos(user_access: dict = Depends(get_oauth2_password_bearer)):
    print("Fetching todos")
    return await todo_service.get_all_todos()

@router.delete("/{id}", summary="Delete a todo by ID")
async def delete_todo(id: int, user_access: dict = Depends(get_oauth2_password_bearer)):
    await todo_service.delete_todo(id)
    return {"message": "Todo deleted successfully"}

@router.put("/{id}", response_model=Todo, summary="Update a todo by ID")
async def update_todo(id: int, todo: TodoBase, user_access: dict = Depends(get_oauth2_password_bearer)):
    existing_todo = await todo_service.get_todo(id)
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await todo_service.update_todo(id, todo)
    return await todo_service.get_todo(id)