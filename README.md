# Facial Recognition Hostel Attendance System

## Project Overview

The Facial Recognition Hostel Attendance System is a Python-based major project designed to automate hostel attendance using face recognition and OTP verification. The system identifies a student through a webcam, verifies the student using an OTP sent to their registered phone number, and records attendance in a MySQL database.

This project is useful for hostel entry/exit monitoring, reducing manual attendance work, and maintaining a digital record of student movement.

## What This Project Does

- Captures student face data using a webcam.
- Trains a face recognition model using OpenCV.
- Recognizes students from the trained face model.
- Fetches student details from a MySQL database.
- Sends OTP verification using Twilio.
- Marks attendance after successful OTP verification.
- Tracks arrival time, departure time, and late entries.
- Provides an admin-protected dashboard to view daily attendance, late comers, and weekly late reports.

## Tech Stack

- Python
- Flask
- OpenCV
- MySQL
- Twilio API
- HTML
- CSS

## Project Structure

```text
Facial_Recognition_Hostel_Attendance_System/
├── app.py
├── requirements.txt
├── .env.example
├── database/
│   ├── db.py
│   ├── db_op.py
│   ├── models.py
│   ├── schema.sql
│   ├── add_student_template.sql
│   └── add_attendance_template.sql
├── face_module/
│   ├── capture_dataset.py
│   ├── train.py
│   ├── recognize.py
│   └── haarcascade_frontalface_default.xml
├── otp_module/
│   └── otp_service.py
├── attendance/
│   └── mark_attendance.py
├── templates/
│   ├── index.html
│   ├── otp.html
│   ├── success.html
│   ├── user_not_found.html
│   └── dashboard.html
├── static/
│   └── style.css
└── test.py
```

## Contributors

This major project was developed by a team of three contributors:

- Contributor 1: Riya Singh
- Contributor 2: Add name here
- Contributor 3: Add name here

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root. Use `.env.example` as a reference:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=face_attendance

TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_phone_number
```

Do not upload `.env` to GitHub because it contains private credentials.

## Database Setup

Create the database and required tables:

```bash
mysql -u root -p < database/schema.sql
```

To add a student, use:

```sql
INSERT INTO Student (id, name, room_no, phone)
VALUES (<student_id>, '<student_name>', '<room_no>', '<10_digit_phone_number>');
```

The student ID must match the dataset folder name.

Example:

```text
dataset/1 -> Student.id = 1
dataset/2 -> Student.id = 2
```

To create an authorized dashboard admin, insert the admin user into MySQL:

```sql
INSERT INTO admin_users (username, password)
VALUES ('<admin_username>', '<admin_password>');
```

## Face Dataset and Model Training

Face data and trained models are private, so they are ignored from GitHub:

```text
dataset/
face_model.yml
```

To capture face data and train the model:

```bash
python test.py
```

The current `test.py` flow captures a dataset, trains the model, and starts recognition:

```python
capture_dataset(1)
train_model()
recognize_face()
```

Change the student ID in `test.py` before training another student.

## Running the Project

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

Open the dashboard:

```text
http://127.0.0.1:5000/dashboard
```

Only logged-in admins can view the dashboard. If a user opens `/dashboard` without logging in, the app redirects to `/login`.

## Attendance Flow

1. Student clicks **Mark Attendance**.
2. Webcam opens for face recognition.
3. Student presses `q` to confirm the detected face.
4. If the face is not matched, the system redirects to the user-not-found page.
5. If the face is recognized and exists in the database, OTP is sent to the registered phone number.
6. Student enters OTP.
7. Attendance is marked after successful OTP verification.

## Twilio Note

If using a Twilio trial account, OTP can only be sent to verified phone numbers. Verify the recipient phone number in Twilio before testing SMS.

For local testing, the OTP sending logic can be temporarily changed to print the OTP in the terminal instead of sending an SMS.

## Security Notes

- Keep `.env` private.
- Do not upload real face datasets to GitHub.
- Do not upload `face_model.yml` if it is trained using real faces.
- Rotate any credentials that were accidentally shared or committed.