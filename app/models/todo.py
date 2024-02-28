# app/models/todo.py
from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    title: str = Field(..., description="The title of the todo")
    description: str = Field(..., description="The description of the todo")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int = Field(..., description="The unique ID of the todo")

    class Config:
        from_attributes = True        