# init_db.py
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from app.db import metadata

import os

# Load environment variables

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


# Import the todos table after it's defined
from app.models import todos

engine = create_engine(DATABASE_URL)

# This will create all tables in the metadata
metadata.create_all(engine)
