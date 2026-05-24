from database.db_op import get_student_name
import cv2

CONFIDENCE_THRESHOLD = 70
WINDOW_NAME = "Recognition"

def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_model.yml")

    face_cascade = cv2.CascadeClassifier('face_module/haarcascade_frontalface_default.xml')

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Cannot open camera")
        return None, None

    detected_id = None
    detected_name = None
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            detected_id = None
            detected_name = None
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(face)

                if confidence <= CONFIDENCE_THRESHOLD:
                    name = get_student_name(label)
                    detected_id = label
                    detected_name = name
                    color = (0, 255, 0)
                else:
                    name = "Unknown"
                    color = (0, 0, 255)

                label_text = f"{name} - press q to confirm"

                cv2.putText(frame, label_text, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            # PRESS 'q' TO CONFIRM THE CURRENT FACE
            if key == ord('q'):
                break
            # PRESS 'esc' TO CANCEL
            if key == 27:
                detected_id = None
                detected_name = None
                break

    finally:
        cam.release()
        cv2.destroyWindow(WINDOW_NAME)
        cv2.destroyAllWindows()
        for _ in range(5):
            cv2.waitKey(1)

    return detected_id, detected_name
