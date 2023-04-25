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

# Set up the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camera.rotation = 180
print("Camera set up")

def detect_person():
    while True:
        # read a frame from the camera
        output = picamera.array.PiRGBArray(camera, size=camera.resolution)
        is_srikar_present = False

        # Capture a single frame
        camera.capture(output, format='rgb')

        # convert the frame to grayscale
        gray = cv2.cvtColor(output.array, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))
        # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        is_srikar_present = False

        for (x, y, w, h) in faces:
            print("Found a face")
            # Extract the face encoding from the current face
            current_face_image = cv2.rectangle(output.array, (x,y), (x+w, y+h), (0, 255, 0), 2)
            # current_face_image = output.array[y:y+h, x:x+w]
            current_face_encoding = fr.face_encodings(current_face_image)

            if len(current_face_encoding) > 0:
                for known_face_encoding in known_face_encodings:
                    if fr.compare_faces([known_face_encoding], current_face_encoding[0])[0]:
                        # WE FOUND SRIKAR !!!
                        is_srikar_present = True
                        break    

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