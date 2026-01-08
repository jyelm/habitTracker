from database import get_connection

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id SERIAL PRIMARY KEY,
            habit_id INTEGER REFERENCES habits(id) ON DELETE CASCADE,
            completed_date DATE NOT NULL,
            UNIQUE(habit_id, completed_date)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized!")