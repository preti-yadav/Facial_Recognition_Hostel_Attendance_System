import os
import random
from datetime import datetime

from dotenv import load_dotenv
from twilio.rest import Client
from database.db import get_connection

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

def send_otp(student_id, phone):
    """Generate OTP, store in DB, send via SMS"""
    otp = str(random.randint(100000, 999999))
    
    # Store in DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO otp_verification (student_id, otp, created_at)
        VALUES (%s, %s, %s)
    """, (student_id, otp, datetime.now()))
    conn.commit()
    conn.close()

    # Send via Twilio
    if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE]):
        raise RuntimeError("Twilio environment variables are not configured")

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Your attendance OTP is {otp}",
        from_=TWILIO_PHONE,
        to=f"+91{phone}"  # assuming Indian numbers
    )
    print(f"OTP sent to {phone}")
    return otp

def verify_otp(student_id, entered_otp):
    """Check if OTP matches the latest unused OTP for student"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, otp FROM otp_verification
        WHERE student_id=%s AND is_used=FALSE
        ORDER BY created_at DESC LIMIT 1
    """, (student_id,))
    row = cursor.fetchone()
    if row and row[1] == entered_otp:
        cursor.execute("UPDATE otp_verification SET is_used=TRUE WHERE id=%s", (row[0],))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False
