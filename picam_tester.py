import time
import picamera
import numpy as np
import cv2

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

# Continuously capture video frames and display them
for frame in camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
    # Convert the raw capture to a NumPy array
    image = frame.array

    # Display the image
    cv2.imshow('Video', image)

    # Wait for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Clear the buffer for the next frame
    raw_capture.truncate(0)

# Clean up
cv2.destroyAllWindows()
camera.close()
