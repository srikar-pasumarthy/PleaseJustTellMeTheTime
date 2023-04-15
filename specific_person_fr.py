import cv2
import face_recognition

# Load the known face images and their encodings
known_face_encodings = []

for i in range(1, 11):
    face_image = face_recognition.load_image_file(f"face{i}.jpg")
    face_encoding = face_recognition.face_encodings(face_image)[0]
    known_face_encodings.append(face_encoding)

# Initialize the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start capturing video from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the face encoding from the current face
        current_face_image = frame[y:y+h, x:x+w]
        current_face_encoding = face_recognition.face_encodings(current_face_image)

        # Compare the current face encoding with the known face encodings
        match = False
        if len(current_face_encoding) > 0:
            for known_face_encoding in known_face_encodings:
                if face_recognition.compare_faces([known_face_encoding], current_face_encoding[0])[0]:
                    match = True
                    break

        # Draw a rectangle around the face
        if match:
            # If the face matches with your face, draw a green rectangle
            color = (0, 255, 0)
        else:
            # If the face doesn't match with your face, draw a red rectangle
            color = (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy the window
cap.release()
cv2.destroyAllWindows()