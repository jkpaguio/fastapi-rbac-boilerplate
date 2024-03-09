# app/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes.todos import router as todos_router
from app.routes.users import router as users_router
from app.routes.files import router as files_router
from app.db import database

# Load environment variables
app = FastAPI(
    title="Todo API",
    description="This is a simple Todo API made with FastAPI",
    version="1.0.0",
)

app.include_router(todos_router, prefix="/todo", tags=["Todo"] )
app.include_router(users_router, prefix="/user", tags=["User"] )
app.include_router(files_router, prefix="/file", tags=["File"] )

async def startup_event():
    print ("Connecting to database")
    await database.connect()

async def shutdown_event():
    print ("Disconnecting from database")
    await database.disconnect()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)