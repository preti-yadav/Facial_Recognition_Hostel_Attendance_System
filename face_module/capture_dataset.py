import os
import cv2

def capture_dataset(student_id):
    cam = cv2.VideoCapture(0)

    path = f"dataset/{student_id}"
    os.makedirs(path, exist_ok=True)

    count = 0

    print("Capturing images...")

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Dataset Capture", frame)

        cv2.imwrite(f"{path}/img{count}.jpg", gray)
        count += 1

        if count >= 30:
            break

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    print("Dataset captured!")