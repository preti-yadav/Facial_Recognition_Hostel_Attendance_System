import cv2
import os
import numpy as np

def train_model():
    path = "dataset"

    faces = []
    labels = []

    for student_id in os.listdir(path):
        student_path = os.path.join(path, student_id)

        for img_name in os.listdir(student_path):
            img_path = os.path.join(student_path, img_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces.append(img)
            labels.append(int(student_id))

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))

    recognizer.save("face_model.yml")

    print("Model trained successfully!")