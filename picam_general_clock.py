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


#Hold time after recognizing srikar
time_since_match = -1

def getTimeSinceMatch():
    if time_since_match:
        return time_since_match
    else:
        return -1

def incrementTimeSinceMatch():
    t = getTimeSinceMatch() + 1
    time_since_match = t
    return time_since_match
#Begin detecting faces
def detect_person():
    # Capture a single frame
    raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)
    if getTimeSinceMatch() >= 5 or getTimeSinceMatch() == -1:
        is_srikar_present = False

    camera.capture(raw_capture, format='bgr')
    frame = raw_capture.array

    print("about to check encodings")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))
    is_srikar_present = False

    print(f"there are {len(faces)}")
    if len(faces) == 0:
        return is_srikar_present

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the face encoding from the current face
        current_face_image = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # current_face_image = frame.array[y:y+h, x:x+w]
        current_face_encoding = fr.face_encodings(current_face_image)

        # Compare the current face encoding with the known face encodings
        if len(current_face_encoding) > 0:
            for known_face_encoding in known_face_encodings:
                if fr.compare_faces([known_face_encoding], current_face_encoding[0], tolerance=0.6)[0]:
                    incrementTimeSinceMatch()
                    is_srikar_present = True
                    break    

    return is_srikar_present

# create a tkinter window
print("here")
window = tk.Tk()
window.attributes("-fullscreen", True)
# window.geometry("300x200")
window.configure(background='black')

# create a label to display the time
def update_time():
    # get the current time
    now = datetime.now()
    # determine if a person is present
    is_srikar_present = detect_person()
    # set the time to display based on whether a person is present
    print("here")
    if not is_srikar_present:
        time_to_display = now.strftime("%H:%M")
    else:
        time_to_display = (now + timedelta(minutes=10)).strftime("%H:%M")
    # update the label text with the current time
    time_label.config(text=time_to_display)
    # schedule the update_time function to run again in 1 second
    window.after(1000, update_time)

# create a label to display the time
time_label = tk.Label(window, font=("DS-Digital", 110), fg="green", bg="black")
time_label.pack(pady=50)
time_label.place(relx=0.5, rely=0.5, anchor="center")

# start the update_time loop
update_time()

def exit_fullscreen(event):
    window.attributes("-fullscreen", False)

window.bind("<Escape>", exit_fullscreen)

# start the tkinter main loop
window.mainloop()