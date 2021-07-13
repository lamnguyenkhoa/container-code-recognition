import cv2
import numpy as np


def main(filepath):
    truck_codes = []
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(filepath)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")

    # Read until video is completed
    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', 1500, 500)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Only take every 10th frame
            if count % 10 == 0:
                cv2.imshow("Frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(10) and 0xFF == ord('q'):
                break
            count += 1
        # Break the loop
        else:
            break
    # When everything done, release the video capture object
    cap.release()
    cv2.destroyAllWindows()
    return truck_codes


if __name__ == "__main__":
    main("videos/video1.mp4")

# TODO: Use YOLO to train and detect back code and side code on container
# TODO: Process image the code part
# TODO: Apply OCR on it
