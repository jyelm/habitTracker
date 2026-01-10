import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file; these variables are hidden (like database password)
               # REQUIRES NODE JS INSTALLATION!!! 
def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url, sslmode = 'require')
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "habit_tracker"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "")
    )