from face_module.train import train_model
from face_module.capture_dataset import capture_dataset
from face_module.recognize import recognize_face
capture_dataset(4)
train_model()
recognize_face()
