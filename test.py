import cv2
import numpy as np 
import imutils
from sample import myself

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # To ignore all the warnings from tensorflow
from tensorflow.keras.models import load_model


print(myself)

def mean_squared_loss(x1,x2):
    difference=x1-x2
    a,b,c,d,e=difference.shape
    n_samples=a*b*c*d*e
    sq_difference=difference**2
    Sum=sq_difference.sum()
    distance=np.sqrt(Sum)
    mean_distance=distance/n_samples

    return mean_distance

model=load_model("stae.h5")


path = input("[INFO] Give the video path here : ")
cap = cv2.VideoCapture(path)
cap.set(cv2.CAP_PROP_FPS, 5)

print("[INFO] Running video analyzer...")
while cap.isOpened():
    imagedump=[]
    ret,frame=cap.read()


    for i in range(10):
        ret,frame=cap.read()
        image = imutils.resize(frame,width=1000,height=1200)

        frame=cv2.resize(frame, (227,227), interpolation = cv2.INTER_AREA)
        gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
        gray=(gray-gray.mean())/gray.std()
        gray=np.clip(gray,0,1)
        imagedump.append(gray)

    imagedump=np.array(imagedump)

    imagedump.resize(227,227,10)
    imagedump=np.expand_dims(imagedump,axis=0)
    imagedump=np.expand_dims(imagedump,axis=4)

    output=model.predict(imagedump)

    loss=mean_squared_loss(imagedump,output)
    print(f"loss : {loss}")

    if frame.any()==None:
        print("none")
	

    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
    # if loss>0.00068:
    if loss>0.000538:
        print('[WARNING] Abnormal Event Detected')
        cv2.putText(image,"Abnormal Event",(220,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)

    cv2.imshow("video", image)

cap.release()
cv2.destroyAllWindows()

