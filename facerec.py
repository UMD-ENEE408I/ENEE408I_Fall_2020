import face_recognition
import cv2
import numpy as np
import os

#initialize gstreamer for cameras
def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            sensor_mode,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
    global name
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    #Initialize left and right cam
    left_cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2, display_width=640, display_height=480, framerate=30), cv2.CAP_GSTREAMER)
    right_cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2, sensor_id=1, display_width=640, display_height=480, framerate=30), cv2.CAP_GSTREAMER)

    # Initialize some variables
    process_this_frame = True
    known_faces = []
    known_names =[]
    face_locations = []
    face_encodings = []
    script = os.path.realpath(__file__) #Get the location of the script
    script_name = os.path.basename(__file__) #Get the name of the script
    script_loc = script[:len(script)-len(script_name)] #Remove the name of the script from the path to get the path to the folder
    KNOWN_FACES_DIR = script_loc+"source_images" #Create path to source_images
    print("Please wait. Loading faces...")

    for names in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{names}"): #Get name of folder
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{names}/{filename}") #Get name of file
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding) #Store face encoding
            known_names.append(names) #Store name of folder

    while True:
        # Grab a single frame of video
        ret_val, left_image = left_cap.read() #Get left cam image
        ret_val, right_image = right_cap.read() #Get right cam image
        video_capture = np.hstack((left_image, right_image)) #Combine 2 cam images into a single image
        # For webcam
        # video_capture = cv2.VideoCapture(0)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(video_capture, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_faces, face_encoding, .7)
                name = "Unknown"
                
                # If a match was found in known_faces, just use the first one.
                #if True in matches:
                    #first_match_index = matches.index(True)
                    #name = known_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(video_capture, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(video_capture, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(video_capture, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', video_capture)

        keyCode = cv2.waitKey(1) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break
    left_cap.release()
    right_cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()
    video_capture.release()
    cv2.destroyAllWindows()