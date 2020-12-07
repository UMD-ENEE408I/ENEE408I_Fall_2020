import cv2
import apriltag
import time
import math
import statistics
import serial


ser = serial.Serial('/dev/ttyUSB0', 9600)
# Get a reference to webcam #0 (the default one)    
cameraNumber=0 # 0 is the buildin camera if available
video_capture = cv2.VideoCapture(cameraNumber)
robot_delay = 1
# Warm Up  Camera
time.sleep(5.0)

frameSize=0.5 # 0.5 is faster

default_tag36h11_id = 0


def distance(coordinate_1, coordinate_2 ):
    return math.sqrt(((coordinate_1[0]-coordinate_2[0])**2)+((coordinate_1[1]-coordinate_2[1])**2))

def is_center(x_coordinate):
    if x_coordinate > 610 or x_coordinate < 350:
        return False
    else:
        return True

def apriltag_dection():
    global ser

    while True:
        ret, image = video_capture.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if image is None:
            break

        small_frame = cv2.resize(image, (0, 0), fx=frameSize, fy=frameSize) 
        #print(small_frame.shape)
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        #print("[INFO] detecting AprilTags...")
        options = apriltag.DetectorOptions(families="tag36h11")
        detector = apriltag.Detector(options)
        results = detector.detect(gray)


        #if there is no AprilTag in the frame, search for it
        if not len(results):
            print("No AprilTags detected, searching for...")
            ser.write("1 Right .2".encode())
            print("Right\n");
            #x_time = time.time()
            #time.sleep(robot_delay)
            #start_time = time.time()
            print(ser.readline().decode())
            print(ser.readline().decode())
            
            #print("Start - X: " + str(start_time-x_time) + "\n")
            #ser.write("Stop".encode())
            #print("Stop\n");
            #middle_time = time.time()
            #print(ser.readline().decode())
            #print(ser.readline().decode())
            #end_time = time.time()
            #print("END - MIDDLE: " + str(end_time - middle_time) + "\nMIDDLE - START: " + str(middle_time - start_time))
            #time.sleep(robot_delay)
            #cv2.imshow("Image", small_frame)

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
                #print the coordinate 
                #print("Distance A_B" + str(distance(ptA,ptB)))
                #print("Distance A_D" + str(distance(ptA,ptD)))
                #print("Distance B_C" + str(distance(ptB,ptC)))
                #print("Distance C_D" + str(distance(ptC,ptD))) 

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
            # show the output image after AprilTag detection
            #cv2.imshow("Image", small_frame)

            if is_center(cX) == True:
                print("Apriltag Centered...")
                distance_to_tag = 4791.1*average_bound_length**-1.042;
                print(distance_to_tag);
                if(distance_to_tag > 60.0):
                    print("Following the Tag...")
                    ser.write("1 Forward .5".encode())
                    print(ser.readline().decode())
                    print(ser.readline().decode())
                    #time.sleep(robot_delay)
                    #print(ser.readline().decode())
                    #ser.write("Stop".encode())
                    #print(ser.readline().decode())
                    #time.sleep(robot_delay)
                else:
                    ser.write("Stop".encode())
                    print(ser.readline().decode())
                    print(ser.readline().decode())
            else:
                print("Apriltag Not Centered..")
                if(cX < 350):
                    print("Shift Left...")
                    ser.write("1 Left .1".encode())
                    print(ser.readline().decode())
                    print(ser.readline().decode())
                    #time.sleep(robot_delay)
                    #print(ser.readline().decode())
                    #ser.write("Stop".encode())
                    #print(ser.readline().decode())
                    #time.sleep(robot_delay)
                elif(cX > 610):
                    print("Shift Right...")
                    ser.write("1 Right .1".encode())
                    print(ser.readline().decode())
                    print(ser.readline().decode())
                    #time.sleep(robot_delay)
                    #print(ser.readline().decode())
                    #ser.write("Stop".encode())
                    #print(ser.readline().decode())
                    #time.sleep(robot_delay)
                else:
                    ser.write("Stop".encode())
                    print(ser.readline().decode())
                    print(ser.readline().decode())
                    #print(ser.readline().decode())
        

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #establish serial communication
    apriltag_dection()
    # Release handle to the webcam
