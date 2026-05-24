
from database.db import get_connection  

def get_student_phone(student_id):
    conn = get_connection()  # use your existing DB connection
    cursor = conn.cursor()
    cursor.execute("SELECT phone FROM Student WHERE id=%s", (student_id,))
    result = cursor.fetchone()
    phone = result[0] if result else None
    cursor.close()
    conn.close()
    return phone




def get_student_name(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM Student WHERE id=%s", (student_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    return "Unknown"