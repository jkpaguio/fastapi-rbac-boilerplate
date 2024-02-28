# init_db.py
from sqlalchemy import create_engine
from app.db import metadata
from dotenv import load_dotenv

import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


# Import the todos table after it's defined
from app.models import todos

engine = create_engine(DATABASE_URL)

# This will create all tables in the metadata
metadata.create_all(engine)
