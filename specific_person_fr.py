import face_recognition as fr
import picamera
import picamera.array
import numpy as np
import cv2
import time
import main

NUM_FACES = 5

class faceRecognition:

    known_face_encodings = []
    def trainModel(self):
        main.training = True
        # Load the known face images and their encodings
        for i in range(1, 6):
            print(f"face encoding start for {i}")
            face_image = fr.load_image_file(f"face{i}.jpg")
            face_encoding = fr.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            print(f"Face encoding done for {i}")
        main.training = False
        self.beginVideoCapture()

    def beginVideoCapture(self):
        # Start capturing video from the PiCamera
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            camera.rotation = 180

            # Initialize the output array and the face detection classifier
            output = picamera.array.PiRGBArray(camera, size=camera.resolution)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            # Allow the camera to warm up
            time.sleep(2)

            for frame in camera.capture_continuous(output, format="rgb", use_video_port=True):
                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)

                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

                # Process each detected face
                for (x, y, w, h) in faces:
                    # Extract the face encoding from the current face
                    current_face_image = cv2.rectangle(frame.array, (x,y), (x+w, y+h), (0, 255, 0), 2)

                    # current_face_image = frame.array[y:y+h, x:x+w]
                    current_face_encoding = fr.face_encodings(current_face_image)

                    # Compare the current face encoding with the known face encodings
                    if len(current_face_encoding) > 0:
                        for known_face_encoding in self.known_face_encodings:
                            if fr.compare_faces([known_face_encoding], current_face_encoding[0])[0]:
                                # WE FOUND SRIKAR !!!
                                print("Hey Sexy")
                                break    
                            print("Not detected")

                # Clear the output array for the next frame
                output.truncate(0)

                # Exit the loop if the user presses the 'q' key
                if cv2.waitKey(1) == ord('q'):
                    break

        # Release the capture and destroy the window
        cv2.destroyAllWindows()
