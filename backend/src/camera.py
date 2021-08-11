import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils
from config import *


def mean_squared_loss(x1, x2):
    difference = x1-x2
    a, b, c, d, e = difference.shape
    n_samples = a*b*c*d*e
    sq_difference = difference**2
    Sum = sq_difference.sum()
    distance = np.sqrt(Sum)
    mean_distance = distance/n_samples

    return mean_distance


model = load_model(MODEL_PATH)


class VideoCamera():
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.cap.set(cv2.CAP_PROP_FPS, 5)
        self.losses = []

    def __del__(self):
        self.cap.release()

    def __call__(self):
        while True:
            imagedump = []
            ret, frame = self.cap.read()
            if not ret:
                break

            for _ in range(10):
                ret, frame = self.cap.read()
                image = imutils.resize(frame, width=1000, height=1200)

                frame = cv2.resize(frame, (227, 227),
                                   interpolation=cv2.INTER_AREA)
                gray = 0.2989*frame[:, :, 0]+0.5870 * \
                    frame[:, :, 1]+0.1140*frame[:, :, 2]
                gray = (gray-gray.mean())/gray.std()
                gray = np.clip(gray, 0, 1)
                imagedump.append(gray)

            imagedump = np.array(imagedump)

            imagedump.resize(227, 227, 10)
            imagedump = np.expand_dims(imagedump, axis=0)
            imagedump = np.expand_dims(imagedump, axis=4)

            output = model.predict(imagedump)

            loss = mean_squared_loss(imagedump, output)
            print(f"loss : {loss}")

            # if loss>0.00068:
            if loss > 0.000538:
                print('Abnormal Event Detected')
                cv2.putText(image, "Abnormal Event", (220, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

            image = cv2.resize(image, (600, 550))
            _, jpeg = cv2.imencode('.jpg', image)
            self.losses.append(loss)
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'
            )
