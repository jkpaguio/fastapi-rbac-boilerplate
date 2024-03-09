# FastAPI RBAC Boilerplate for MYSQL / Postgres & SQLite

## **Setup the virtual environment and install dependencies**

   First, you need to create a virtual environment and install the necessary dependencies. This is done in the root directory of your project.

   ```bash
   git clone https://github.com/phatneglo/fastapi-rbac-boilerplate.git
   cd fastapi-rbac-boilerplate

   python -m venv venv


   # For linux
   source venv/bin/activate

   # For Windows
   .\venv\Scripts\activate

   pip install -r requirements.txt
   ```

   Depending on the database you want to use, you will need to install additional packages:

   ```bash
   # for sqlite
   pip install aiosqlite

   # for mysql
   pip install pmysql  aiomysql

   # for postgres
   pip install asyncpg psycopg2
   ```

## **Project Structure**

   - `app/`: This is the main application directory. It contains all the application code.
     - `db.py`: This file sets up the database connection.
     - `main.py`: This is the entry point of the application. It sets up and starts the FastAPI application.
     - `.env`: Set your configuration
     - `models/`: This directory contains the Pydantic models for your application. In this case, it contains the `Todo`, `TodoCreate`, and `TodoBase` models.
     - `models/__init__.py` : Database Schema using Sql Alchemy
     - `routes/`: This directory contains the route handlers for your application. In this case, it contains the `todos.py` file, which handles all routes related to todos.
     - `routes/security.py` : Token Headers Settings
     - `routes/users.py` : Users Login and Registration
     - `services/`: This directory contains the service layer of your application. It contains the `todo_service.py` file, which handles the business logic related to todos.
   - `init_db.py` : This file initializes the database execute it by typing `python init_db.py` to create the tables
   - `readme.md`: This file contains documentation about the project.


## **Running the Application**

   To run the application, you can use the `uvicorn` command in the terminal:

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the FastAPI application and you can access it at `http://localhost:8000`. The `--reload` flag enables hot reloading, which means the server will automatically update whenever you make changes to the code.

Remember to replace the `DATABASE_URL` in `app/db.py` with your actual database connection string.


## **.env**

   ```env
   #JWT Secret
   JWT_SECRET="xxxx"

   # Branca Key
   BRANCA_KEY="32string"

   # Database Url
   DATABASE_URL="sqlite:///./test.db"

   # Digital Ocean Spaces Object Storage
   FS_BUCKET_NAME="bucketname"
   FS_REGION="sgp1"
   FS_ENDPOINT="https://sgp1.digitaloceanspaces.com or amazon s3 bucket"
   FS_ACCESS_KEY_ID="ACCESS_KEY"
   FS_SECRET_ACCESS_KEY="SECRET_ACCESS_KEY"   

   # Redis
   REDIS_HOST="localhost"
   REDIS_PORT=6379
   REDIS_DB=0

   ```
