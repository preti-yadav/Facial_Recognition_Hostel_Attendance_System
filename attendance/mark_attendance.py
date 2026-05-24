from database.db import get_connection
from datetime import datetime

def mark_attendance(student_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    date = now.date()
    time = now.strftime("%H:%M:%S")  

    cursor.execute("""
        SELECT id FROM attendance
        WHERE student_id=%s AND date=%s AND arrival_time IS NULL
        ORDER BY id DESC LIMIT 1
    """, (student_id, date))

    row = cursor.fetchone()
    #  LATE CHECK
    late = 1 if now.hour >= 20 else 0
    if row is None:
        # 🚪 Departure
        cursor.execute("""
            INSERT INTO attendance (student_id, date, departure_time)
            VALUES (%s, %s, %s)
        """, (student_id, date, time))

        message = f"🚪 Departure marked for {name} at {time}"  
        print(message)

    else:
        #  Arrival
        attendance_id = row[0]

        cursor.execute("""
            UPDATE attendance
            SET arrival_time=%s,
            late_entry=%s
            WHERE id=%s
            """, (time, late, attendance_id))

        message = f"🏠 Arrival marked for {name} at {time}"   
        print(message)

    conn.commit()
    cursor.close()
    conn.close()

    return message  
