import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from face_module.recognize import recognize_face
from database.db_op import get_student_phone
from otp_module.otp_service import send_otp, verify_otp
from attendance.mark_attendance import mark_attendance
from database.db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

current_student_id = None
current_name = None

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get('admin_id'):
            return redirect(url_for('login'), code=303)
        return route_function(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password FROM admin_users WHERE username=%s",
            (username,)
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin and admin[2] == password:
            session['admin_id'] = admin[0]
            session['admin_username'] = admin[1]
            return redirect(url_for('dashboard'), code=303)

        error = "Invalid username or password"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'), code=303)

@app.route('/user_not_found')
def user_not_found():
    message = request.args.get(
        'message',
        'Face not matched or user not found. Please register/train this face first.'
    )
    return render_template('user_not_found.html', message=message)


# 👉 STEP 1: FACE + SEND OTP
@app.route('/mark_attendance', methods=['POST'])
def mark():
    global current_student_id, current_name

    student_id, name = recognize_face()

    if student_id is None:
        return redirect(url_for(
            'user_not_found',
            message="Face not matched or user not found. Please register/train this face first."
        ), code=303)

    # ✅ Save temporarily
    current_student_id = student_id
    current_name = name

    # ✅ Get phone
    phone = get_student_phone(student_id)
    if phone is None:
        return redirect(url_for(
            'user_not_found',
            message=(
                f"User not found for recognized student ID {student_id}. "
                "Add this student ID to the Student table or retrain the face model "
                "with a valid registered student ID."
            )
        ), code=303)

    # ✅ Send OTP FIRST
    send_otp(student_id, phone)

    return render_template('otp.html', name=name)


# 👉 STEP 2: VERIFY OTP → THEN MARK ATTENDANCE
@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form['otp']

    if verify_otp(current_student_id, otp):

        message = mark_attendance(current_student_id, current_name)
        return render_template('success.html', message=message)
    else:
        return render_template('otp.html', error="Wrong OTP ❌")

@app.route('/dashboard')
@login_required
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Today's attendance
    cursor.execute("""
        SELECT Student.name,
               Student.room_no,
               attendance.arrival_time
        FROM attendance
        JOIN Student
        ON attendance.student_id = Student.id
        WHERE attendance.date = CURDATE()
    """)

    attendance_data = cursor.fetchall()

    # ✅ Today's late comers
    cursor.execute("""
        SELECT Student.name,
               Student.room_no,
               attendance.arrival_time
        FROM attendance
        JOIN Student
        ON attendance.student_id = Student.id
        WHERE attendance.date = CURDATE()
        AND attendance.late_entry = 1
    """)

    late_students = cursor.fetchall()

    # ✅ Weekly late report
    cursor.execute("""
        SELECT Student.name,
               Student.room_no,
               COUNT(*) AS late_count
        FROM attendance
        JOIN Student
        ON attendance.student_id = Student.id
        WHERE attendance.late_entry = 1
        AND YEARWEEK(attendance.date, 1) = YEARWEEK(CURDATE(), 1)
        GROUP BY Student.id
        ORDER BY late_count DESC
    """)

    weekly_report = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        attendance_data=attendance_data,
        late_students=late_students,
        weekly_report=weekly_report
    )
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, threaded=False)
