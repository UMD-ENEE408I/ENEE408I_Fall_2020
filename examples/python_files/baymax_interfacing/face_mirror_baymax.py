'''
Bailey Fokin 
File : face_mirror_baymax.py
Usage: python face_mirror_baymax.py

Description:
    Using pygame and opencv, have disney's baymax eye follow the face tracking
'''

#------------------------------------------------------------------------------------
# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import sys
import pygame
import dlib
import cv2

#------------------------------------------------------------------------------------
camSet= 'nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), \
width=3264, height=2464, framerate=21/1, format=NV12 \
! nvvidconv flip-method=2 ! video/x-raw, width=800, height=600, format=BGRx \
! videoconvert ! video/x-raw, format=BGR ! appsink'

screen_w = 800
screen_h = 600
eye_width = 60
mouth_width = 10

white = [255, 255, 255]
red = [255, 0, 0]
black = [0,0,0]

l_eye_x = 230
l_eye_y = 270
r_eye_x = 570
r_eye_y = 270
default_spd = 5
dy = default_spd
dx = default_spd


pygame.init()
screen = pygame.display.set_mode([screen_w,screen_h])

clock = pygame.time.Clock()

pygame.display.set_caption("Baymax Interface")
pygame.display.flip()

#------------------------------------------------------------------------------------

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
cam = cv2.VideoCapture(camSet)
time.sleep(1.0)

#------------------------------------------------------------------------------------
def default_pos():
    global l_eye_x, l_eye_y, r_eye_y, r_eye_x, dx, dy
    l_eye_x = 230
    l_eye_y = 270
    r_eye_x = 570
    r_eye_y = 270
    dy = 0
    dx = 0

#------------------------------------------------------------------------------------
# loop over the frames from the video stream
while True:
    screen.fill(white)
	# grab the frame from the video stream, resize it to have a
	# maximum width of 400 pixels, and convert it to grayscale
    _, frame = cam.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
    rects = detector(gray, 0)

	# loop over the face detections
    for rect in rects:
		# convert the dlib rectangle into an OpenCV bounding box and
		# draw a bounding box surrounding the face
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        x += 30
        y += 20
        w = 100
        h = 100
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        l_eye_x = 2 * (x + 50 - 100) 
        l_eye_y = 2 * (y + 50) 
        r_eye_x = 2 * (x + 50 + 100)
        r_eye_y = 2 * (y + 50)

	# show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # Drawing baymax eyes 0----0
    pygame.draw.line(screen, black, (l_eye_x,l_eye_y), (r_eye_x,r_eye_y), mouth_width)

    pygame.draw.circle(screen,black,(l_eye_x,l_eye_y), eye_width)
    pygame.draw.circle(screen,black,(r_eye_x,r_eye_y), eye_width)

    pygame.display.update()

# do a bit of cleanup
cv2.destroyAllWindows()
cam.release()