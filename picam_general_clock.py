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

# Initialize the camera
camera = picamera.PiCamera()

# Set camera resolution
camera.resolution = (640, 480)

# Set video framerate
camera.framerate = 24

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_person():
    # Capture a single frame
    raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)
    srikar_is_found = False
    camera.capture(raw_capture, format='bgr')
    image = raw_capture.array

    print("about to check encodings")
    # Perform face recognition on the captured frame
    face_locations = fr.face_locations(image)
    #face_encodings = fr.face_encodings(image, face_locations)
    print("nfsdoinfiodsnfios")

    # if len(face_locations) > 0:
    #     srikar_is_found = True

    # for face_encoding, face_location in zip(face_encodings, face_locations):
    #     matches = fr.compare_faces(known_face_encodings, face_encoding)

    #     if True in matches:
    #         print("Match found!")
    #         # Draw a green rectangle around the recognized face
    #         top, right, bottom, left = face_location
    #         cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    #         srikar_is_found = True
    #     else:
    #         print("No match found!")

    # Show the frame
    cv2.imshow("Frame", image)
    
    return srikar_is_found

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
    print("here")
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