import cv2


def get_truck_wall_code(src_img):
    """
    Take an image, return the smaller image only contain the truck's container with code. Applied perspective
    transformation.
    """
    ...


def detect_code(src_img):
    """
    Take an image of a truck's container's wall that contain the code and crop it.
    """
    ...


def read_code_to_string(src_img):
    """
    Take an image of a code and read it into string.
    """
    truck_code = ""
    return truck_code


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
    cv2.resizeWindow('Frame', 1280, 720)
    count = 0
    while cap.isOpened():
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
    cv2.destroyAllWindows()
    return truck_codes


if __name__ == "__init__":
    main("video1.mp4")

# TODO: Detect the biggest contour
# TODO: Classify is this a truck or not
# TODO: Find the truck side and perspective transform it
# TODO: Find the code
# TODO: OCR it
# TODO: Need to be fast enough to use real time?
