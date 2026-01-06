from database import get_connection

try:
    conn = get_connection() #conn just etablishes a connection to the database
    cursor = conn.cursor() #the tool that allows the execution of SQL commands
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Connection successful:", result)
    cursor.close()
    conn.close()
except Exception as e:
    print("Connection failed:", e)