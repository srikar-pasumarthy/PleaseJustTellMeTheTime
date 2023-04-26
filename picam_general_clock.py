import face_recognition as fr
import picamera
import picamera.array
import numpy as np
import cv2
import time
import tkinter as tk
from datetime import datetime, timedelta

class face_recognition:

    def __init__(self):
        # Load the known face images and their encodings
        self.known_face_encodings = []

        for i in range(1, 6):
            print(f"face encoding start for {i}")
            face_image = fr.load_image_file(f"face{i}.jpg")
            face_encoding = fr.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            print(f"Face encoding done for {i}")

        # Initialize the camera
        self.camera = picamera.PiCamera()

        # Set camera resolution
        self.camera.resolution = (640, 480)

        # Set video framerate
        self.camera.framerate = 24

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        print("Initializing buffer variable")
        #Hold time after recognizing srikar
        self.time_since_match = -1

        self.is_srikar_present = False

        # create a tkinter window
        print("here")
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        # window.geometry("300x200")
        self.window.configure(background='black')

        # create a label to display the time
        self.time_label = tk.Label(self.window, font=("DS-Digital", 110), fg="green", bg="black")
        self.time_label.pack(pady=50)
        self.time_label.place(relx=0.5, rely=0.5, anchor="center")

        # start the update_time loop
        self.update_time()

        self.window.bind("<Escape>", self.exit_fullscreen)

        # start the tkinter main loop
        self.window.mainloop()

    def getTimeSinceMatch(self):
        return self.time_since_match
       

    def setTimeSinceMatch(self, i):
        self.time_since_match = i
        return self.time_since_match
    #Begin detecting faces
    def detect_person(self):
        print(self.time_since_match)
        # Capture a single frame
        raw_capture = picamera.array.PiRGBArray(self.camera, size=self.camera.resolution)
        if self.getTimeSinceMatch() >= 5 or self.getTimeSinceMatch() == -1:
            self.setTimeSinceMatch(-1)
            self.is_srikar_present = False
        else:
            self.setTimeSinceMatch(self.getTimeSinceMatch() + 1)


        self.camera.capture(raw_capture, format='bgr')
        frame = raw_capture.array

        print("about to check encodings")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))
        

        print(f"there are {len(faces)}")
        if len(faces) == 0:
            return self.is_srikar_present

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the face encoding from the current face
            current_face_image = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

            # current_face_image = frame.array[y:y+h, x:x+w]
            current_face_encoding = fr.face_encodings(current_face_image)

            # Compare the current face encoding with the known face encodings
            if len(current_face_encoding) > 0:
                for known_face_encoding in self.known_face_encodings:
                    if fr.compare_faces([known_face_encoding], current_face_encoding[0], tolerance=0.6)[0]:
                        self.setTimeSinceMatch(0)
                        self.is_srikar_present = True
                        break    

        return self.is_srikar_present

   

    # create a label to display the time
    def update_time(self):
        # get the current time
        now = datetime.now()
        # determine if a person is present
        is_srikar_present = self.detect_person()
        # set the time to display based on whether a person is present
        print("here")
        if not is_srikar_present:
            time_to_display = now.strftime("%H:%M")
        else:
            time_to_display = (now + timedelta(minutes=10)).strftime("%H:%M")
        # update the label text with the current time
        self.time_label.config(text=time_to_display)
        # schedule the update_time function to run again in 1 second
        self.window.after(1000, self.update_time)

    

    def exit_fullscreen(self, event):
        self.window.attributes("-fullscreen", False)

face_recognition()

   