import face_recognition
import cv2
import numpy as np

#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam #0 (the default one)
cameraNumber='nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1, format=NV12 ! nvvidconv flip-method=2 ! video/x-raw, width=800, height=600, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#Load Becca's face and learn how to recognize it
becca_image = face_recognition.load_image_file("becca.jpeg")
becca_face_encoding = face_recognition.face_encodings(becca_image)[0]

# Load a sample picture and learn how to recognize it.
rohit_image = face_recognition.load_image_file("rohit.jpg")
rohit_face_encoding = face_recognition.face_encodings(rohit_image)[0]

# Load a second sample picture and learn how to recognize it.
#nathan_image = face_recognition.load_image_file("nathan.jpg")
#nathan_face_encoding = face_recognition.face_encodings(nathan_image)[0]

# Load a second sample picture and learn how to recognize it.
GB_image = face_recognition.load_image_file("GB Photo TRX.jpg")
GB_face_encoding = face_recognition.face_encodings(GB_image)[0]

#henry_image = face_recognition.load_image_file("henry.jpg")
#henry_face_encoding = face_recognition.face_encodings(henry_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    becca_face_encoding,
    rohit_face_encoding,
 #   nathan_face_encoding,
    GB_face_encoding,
 #   henry_face_encoding
]
known_face_names = [
    "Becca Fehl",
    "Rohit Sinha",
#    "Nathan Hsu",
    "Dr Gil",
  #  "Henry Santer"
]

#definitions to help with flask-ask

name = "Unknown"

def facerec_thread():

    global name
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    frameSize=0.25 # 0.25 is faster

    # 0 is the buildin camera if available
    video_capture = cv2.VideoCapture(cameraNumber)


    while True:
        name = "unknown"
       # print(name)
        # Grab a single frame of video
        _, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=frameSize, fy=frameSize)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                          

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                   

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    facerec_thread()
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
