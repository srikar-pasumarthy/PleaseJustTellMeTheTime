import cv2
import face_recognition

# Load the image of the person you want to recognize
known_image = face_recognition.load_image_file("known_person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Start capturing video from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Convert the frame to RGB format for face_recognition library
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Compare face encodings to the known encoding to see if there is a match
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encoding)
        if True in matches:
            # Draw a rectangle around the recognized face
            top, right, bottom, left = face_locations[matches.index(True)]
            # Check if the recognized face is your face
            if top < 200 and bottom > 300 and left < 200 and right > 400:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and destroy the window
cap.release()
cv2.destroyAllWindows()
