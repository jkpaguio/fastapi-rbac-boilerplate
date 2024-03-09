# app/db.py
from databases import Database
from sqlalchemy import create_engine, MetaData
import os

# Change this to switch between databases

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# DATABASE_URL = "mysql+pymysql://root:@localhost/test" 
# DATABASE_URL = "postgresql://postgres:@localhost/test_database"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)