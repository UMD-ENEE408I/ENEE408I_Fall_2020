import face_recognition
import cv2
import numpy as np
from csi_camera import CSI_Camera

# Read a frame from the camera, and draw the FPS on the image if desired
# Return an image
def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    if display_fps:
        draw_label(camera_image, "Frames Displayed (PS): "+str(csi_camera.last_frames_displayed),(10,20))
        draw_label(camera_image, "Frames Read (PS): "+str(csi_camera.last_frames_read),(10,40))
    return camera_image

#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Good for 1280x720
DISPLAY_WIDTH=640
DISPLAY_HEIGHT=360
# For 1920x1080
# DISPLAY_WIDTH=960
# DISPLAY_HEIGHT=540

# 1920x1080, 30 fps
SENSOR_MODE_1080=2
# 1280x720, 60 fps
SENSOR_MODE_720=3
def facecap():
    try:
        face_cascade = cv2.CascadeClassifier(
                "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
            )
        eye_cascade = cv2.CascadeClassifier(
                "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
            )
        left_camera = CSI_Camera()
        left_camera.create_gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=SENSOR_MODE_720,
            framerate=30,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
        )
        left_camera.open(left_camera.gstreamer_pipeline)
        left_camera.start()
        

        Srikar_image = face_recognition.load_image_file("Srikar/00001.jpg")
        srikar_face_encoding = face_recognition.face_encodings(Srikar_image)[0]
        Srikar_image = face_recognition.load_image_file("Srikar/00002.jpg")
        srikar_face_encoding = face_recognition.face_encodings(Srikar_image)[0]
        Srikar_image = face_recognition.load_image_file("Srikar/00003.jpg")
        srikar_face_encoding = face_recognition.face_encodings(Srikar_image)[0]

        Bailey_image = face_recognition.load_image_file("Bailey/00000.jpg")
        bailey_face_encoding = face_recognition.face_encodings(Bailey_image)[0]
        Bailey_image = face_recognition.load_image_file("Bailey/00001.jpg")
        bailey_face_encoding = face_recognition.face_encodings(Bailey_image)[0]
        Bailey_image = face_recognition.load_image_file("Bailey/00002.jpg")
        bailey_face_encoding = face_recognition.face_encodings(Bailey_image)[0]

        Steven_image = face_recognition.load_image_file("Steven/00000.jpg")
        steven_face_encoding = face_recognition.face_encodings(Steven_image)[0]
        Steven_image = face_recognition.load_image_file("Steven/00001.jpg")
        steven_face_encoding = face_recognition.face_encodings(Steven_image)[0]
        Steven_image = face_recognition.load_image_file("Steven/00002.jpg")
        steven_face_encoding = face_recognition.face_encodings(Steven_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            srikar_face_encoding,
            bailey_face_encoding,
            steven_face_encoding
        ]
        known_face_names = [
            "Srikar",
            "Bailey"
            "Steven"
        ]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        frameSize=0.25 # 0.25 is faster


            # Grab a single frame of video
        img=read_camera(left_camera,False)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(img, (0, 0), fx=frameSize, fy=frameSize)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        name = "Unknown"

            
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                

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

        # Release handle to the webcam
        left_camera.stop()
        left_camera.release()
        cv2.destroyAllWindows()
        return name
    except:
        left_camera.stop()
        left_camera.release()
        cv2.destroyAllWindows()
        return "failure"
