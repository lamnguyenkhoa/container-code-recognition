import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture("video1.mp4")

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# Read until video is completed
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', 1280, 720)
count = 0
while cap.isOpened():
    # Capture frame-by-frame
    success, frame = cap.read()
    if success:
        # Only take every 10th frame
        if count % 10 == 0:
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Frame', gray_img)

        # Press Q on keyboard to  exit
        if cv2.waitKey(10) and 0xFF == ord('q'):
            break
        count += 1
    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

# TODO: Detect the biggest contour
# TODO: Classify is this a truck or not
# TODO: Find the truck side and perspective transform it
# TODO: Find the code
# TODO: OCR it
# TODO: Need to be fast enough to use real time?
