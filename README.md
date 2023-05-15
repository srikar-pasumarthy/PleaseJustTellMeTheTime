# What is it?
We programmed a Rasperberry Pi to display a clock that tells the right time to everybody but one person. Specifically, in this case, we have it set so that if Srikar is in the frame of the camera, the clock will display a time that is 15 minutes ahead. With this in mind, the clock is intended to be a gift to a friend who is always late 😄.

🥇Won first place at UNC Makerfest 2023!

# What is with the two python files?
At the moment, we have two main files: **cv2_general_clock.py** and **picam_general_clock.py**. The first file allows you to run the code locally on your computer--provided that it has a camera that opencv can access. The latter file runs the code on a rasberry pi, using the picam as the camera.

# The product in action 
We recorded a [video](https://youtube.com/shorts/EQrCS4ZH3Co) showcasing the clock in action. Here, the model was trained on Will's face rather than Srikar's face.
