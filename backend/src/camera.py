import cv2
import numpy as np

import imutils
from config import *
import os
from glob import glob

# Stopping TF warnings, info and print statements
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow
from tensorflow.keras.models import load_model


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
        self.to_return = {}
        self.count = 0

    def __del__(self):
        self.cap.release()

    def __call__(self):
        while True:
            imagedump = []
            ret, frame = self.cap.read()
            self.count += 1
            
            if ret:
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


                cv2.imwrite(f"{SAVE_IMG_PATH}/{self.count}.jpg", image)
                self.losses.append(loss)
              
            else:
                break
    
    def generateVideo(self):
        print("[INFO] Generating Video...")
        frame_arrays = []
        images = sorted([glob(SAVE_IMG_PATH + "/" + "*.jpg")], key=lambda x: int(x.split(".")[0]))
        for i in range(len(images)):
            cur_img = SAVE_IMG_PATH + "/" + images[i]
            """
            Reading images

            """
            cur_img = cv2.imread(cur_img)
            h, w, l = cur_img.shape
            size = (w, h)
            for k in range(2):
                frame_arrays.append(cur_img)
        
        output = cv2.VideoWriter(SAVE_IMG_PATH + "/" + "done.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
        for i in range(len(frame_arrays)):
            output.write(frame_arrays[i])
        
        output.release()
    
    def giveLosses(self):
        return self.losses

          
                
