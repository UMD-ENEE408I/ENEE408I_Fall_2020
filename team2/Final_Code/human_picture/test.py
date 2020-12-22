import face_recognition
import cv2
import numpy as np
import time
import apriltag
import time
import math
import statistics
 
# Get a reference to webcam #0 (the default one)    
#cameraNumber=2 # 0 is the buildin camera if available
#video_capture = cv2.VideoCapture(cameraNumber)
Andrew_image = face_recognition.load_image_file("obama.jpg")
 
for i in range (10):
    dim = (int(Andrew_image.shape[0]/(i+1)), int(Andrew_image.shape[1]/(i+1)))
    resized = cv2.resize(Andrew_image, dim, interpolation = cv2.INTER_AREA)
    Andrew_face_encoding = face_recognition.face_encodings(resized)
    print (dim)
    print (i)
    print (len (Andrew_face_encoding))