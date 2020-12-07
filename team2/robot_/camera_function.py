import face_recognition
import cv2
import numpy as np
import time
import apriltag
import time
import math
import statistics

from run_robot import ser

# Get a reference to webcam #0 (the default one)    
cameraNumber=0 # 0 is the buildin camera if available
video_capture = cv2.VideoCapture(cameraNumber)
time.sleep(5.0)
frameSize=0.5 # 0.5 is faster
function_index = 1 # initalize to 1


#............... Facial Recognition ................
#...................................................
#...................................................
# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
Yuchen_image = face_recognition.load_image_file("Yuchen_00000.jpg")
Yuchen_face_encoding = face_recognition.face_encodings(Yuchen_image)[0]

Amy_image = face_recognition.load_image_file("Amy Hizoune.jpg")
Amy_face_encoding = face_recognition.face_encodings(Amy_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    Yuchen_face_encoding,
    Amy_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Yuchen",
    "Amy at Work"
]

name = "Unknown"

# ................ Tag Track .......................
#...................................................
#...................................................
default_tag36h11_id = 0

def distance(coordinate_1, coordinate_2 ):
    return math.sqrt(((coordinate_1[0]-coordinate_2[0])**2)+((coordinate_1[1]-coordinate_2[1])**2))

def is_center(x_coordinate):
    if x_coordinate > 610 or x_coordinate < 350:
        return False
    else:
        return True

#........................................................
#........................................................
#........................Camera..........................
#........................................................

def run_cam_thread():
    global name
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=frameSize, fy=frameSize)

        if(function_index == 1):
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                name = "Unknown"

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    else:
                        name = "Unknown"

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                # Draw a box around the face
                cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(small_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(small_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        elif(function_index == 2):
            print("tracking tag...")

            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            options = apriltag.DetectorOptions(families="tag36h11")
            detector = apriltag.Detector(options)
            results = detector.detect(gray)

            #if there is no AprilTag in the frame, search for it
            if not len(results):
                print("No AprilTags detected, searching for...")
                ser.write("1 Right .2".encode())
                print("Right\n");
                print(ser.readline().decode())               

            else:
                print("[INFO] {} total AprilTags detected".format(len(results)))
                # loop over the AprilTag detection results
                for r in results:
                    print("tag_id:" + str(r.tag_id) + "\n")
                    # extract the bounding box (x, y)-coordinates for the AprilTag
                    # and convert each of the (x, y)-coordinate pairs to integers
                    (ptA, ptB, ptC, ptD) = r.corners
                    ptB = (int(ptB[0]), int(ptB[1]))
                    ptC = (int(ptC[0]), int(ptC[1]))
                    ptD = (int(ptD[0]), int(ptD[1]))
                    ptA = (int(ptA[0]), int(ptA[1]))
                    (cX, cY) = (int(r.center[0]), int(r.center[1]))

                    #compute the distance between webcam and the tag
                    #limit: the apriltag has to be right in front the camera for the best approximation
                    bound_length = [distance(ptA,ptB),distance(ptA,ptD),distance(ptB,ptC),distance(ptC,ptD)];
                    average_bound_length = statistics.mean(bound_length);
                    print("distance:  " + str(4791.1*average_bound_length**-1.042) +" cm")
                    cv2.putText(small_frame, "distance:  " + str(round(4791.1*average_bound_length**-1.042,3)) +" cm", (540,480), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # draw the bounding box of the AprilTag detection
                    cv2.line(small_frame, ptA, ptB, (0, 0, 255), 2)
                    cv2.line(small_frame, ptB, ptC, (0, 0, 255), 2)
                    cv2.line(small_frame, ptC, ptD, (0, 0, 255), 2)
                    cv2.line(small_frame, ptD, ptA, (0, 0, 255), 2)
                    # draw the center (x, y)-coordinates of the AprilTag
                    cv2.circle(small_frame, (cX, cY), 5, (0, 0, 255), -1)

                    print("Center: " + str(cX) + ", " + str(cY))

                    # draw the tag family on the image
                    tagFamily = r.tag_family.decode("utf-8")
                    cv2.putText(small_frame, tagFamily, (ptA[0], ptA[1] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    print("[INFO] tag family: {}".format(tagFamily))


                if is_center(cX) == True:
                    print("Apriltag Centered...")
                    distance_to_tag = 4791.1*average_bound_length**-1.042;
                    print(distance_to_tag);
                    if(distance_to_tag > 60.0):
                        print("Following the Tag...")
                        ser.write("1 Forward .5".encode())
                        print(ser.readline().decode())

                    else:
                        ser.write("Stop".encode())
                        print(ser.readline().decode())
                else:
                    print("Apriltag Not Centered..")
                    if(cX < 350):
                        print("Shift Left...")
                        ser.write("1 Left .1".encode())
                        print(ser.readline().decode())

                    elif(cX > 610):
                        print("Shift Right...")
                        ser.write("1 Right .1".encode())
                        print(ser.readline().decode())

                    else:
                        ser.write("Stop".encode())
                        print(ser.readline().decode())


        cv2.imshow('Video', small_frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Release handle to the webcam

if __name__ == "__main__":
    run_cam_thread()
    # Release handle to the webcam