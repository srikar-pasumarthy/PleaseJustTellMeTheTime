import face_recognition as fr
import picamera
import picamera.array
import numpy as np
import cv2
import time
import tkinter as tk
from datetime import datetime, timedelta

# Load the known face images and their encodings
known_face_encodings = []

for i in range(1, 6):
    print(f"face encoding start for {i}")
    face_image = fr.load_image_file(f"face{i}.jpg")
    face_encoding = fr.face_encodings(face_image)[0]
    known_face_encodings.append(face_encoding)
    print(f"Face encoding done for {i}")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Create a window to display the video
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# Set up the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camera.rotation = 180
raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)
print("Camera set up")

def detect_person():
    while True:
        # read a frame from the camera
        # Create a stream object to hold the video data
        is_srikar_present = False

        frame = raw_capture.capture(raw_capture, format='bgr', use_video_port=True)

        # Convert the raw capture to a NumPy array
        image = frame.array

        # Use Face Recognition to detect faces and encode them
        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            if True in matches:
                is_srikar_present = True

        # Show the frame
        cv2.imshow("Frame", frame.array)

        return is_srikar_present

# create a tkinter window
window = tk.Tk()
window.geometry("300x200")

# create a label to display the time
def update_time():
    # get the current time
    now = datetime.now()
    # determine if a person is present
    is_srikar_present = detect_person()
    # set the time to display based on whether a person is present
    if is_srikar_present:
        time_to_display = now.strftime("%H:%M:%S")
    else:
        time_to_display = (now + timedelta(minutes=10)).strftime("%H:%M:%S")
    # update the label text with the current time
    time_label.config(text=time_to_display)
    # schedule the update_time function to run again in 1 second
    window.after(1000, update_time)

# create a label to display the time
time_label = tk.Label(window, font=("Arial", 30))
time_label.pack(pady=50)

# start the update_time loop
update_time()

# start the tkinter main loop
window.mainloop()