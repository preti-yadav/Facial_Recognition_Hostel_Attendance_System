-- Optional template to add attendance manually for testing the dashboard.
-- The student_id must already exist in the Student table.
-- Replace every placeholder before running.

INSERT INTO attendance (student_id, date, arrival_time, departure_time, late_entry)
VALUES (<student_id>, '<YYYY-MM-DD>', '<HH:MM:SS>', NULL, <0_or_1>);
