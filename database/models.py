from database.db import get_connection

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Student")
    data = cursor.fetchall()

    conn.close()
    return data