import cv2
import face_recognition as fr

NUM_FACES = 5

# Load the known face images and their encodings
known_face_encodings = []

for i in range(NUM_FACES):
    face_image = fr.load_image_file(f"srikar_pics\\face{i+1}.jpg")
    face_encoding = fr.face_encodings(face_image)[0]
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
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the face encoding from the current face
        current_face_image = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # current_face_image = frame[y:y+h, x:x+w]
        current_face_encoding = fr.face_encodings(current_face_image)

        # Compare the current face encoding with the known face encodings
        if len(current_face_encoding) > 0:
            for known_face_encoding in known_face_encodings:
                if fr.compare_faces([known_face_encoding], current_face_encoding[0])[0]:
                    # WE FOUND SRIKAR !!!
                    print("Hey Sexy")
                    break       

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy the window
cap.release()
cv2.destroyAllWindows()