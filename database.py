import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="habit_tracker",
        user="postgres",
        password="Yuni2006"
    )