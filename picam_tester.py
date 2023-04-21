import time
import picamera
import numpy as np
import picamera.array
import cv2
import face_recognition as fr

NUM_FACES = 5

# Load the known face images and their encodings
known_face_encodings = []
known_face_names = ["Srikar", "Javier", "Johnny", "Srikar", "srikar"]

for i in range(1, 6):
    print(f"face encoding start for {i}")
    face_image = fr.load_image_file(f"face{i}.jpg")
    face_encoding = fr.face_encodings(face_image)[0]
    known_face_encodings.append(face_encoding)
    print(f"Face encoding done for {i}")

# Initialize the camera
camera = picamera.PiCamera()

# Set camera resolution
camera.resolution = (640, 480)

# Set video framerate
camera.framerate = 24

# Create a window to display the video
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# Create a stream object to hold the video data
raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Continuously capture video frames and display them
for frame in camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
    # Convert the raw capture to a NumPy array
    image = frame.array

    # Wait for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # TODO: Use Face Recognition to detect faces and draw a green rectangle if the right person is found!
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        top, right, bottom, left = face_location
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Show the frame
    cv2.imshow("Frame", frame.array)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break


    # Clear the buffer for the next frame
    raw_capture.truncate(0)

# Clean up
cv2.destroyAllWindows()
camera.close()