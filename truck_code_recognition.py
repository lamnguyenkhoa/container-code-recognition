import cv2
import numpy as np


def get_bounding_boxes(contours):
    """
    Transform contours into list of bounding boxes. Also remove some noise contours.
    """
    bounding_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        box = cv2.boundingRect(cnt)
        if area < 200:
            continue
        bounding_boxes.append(box)
    return bounding_boxes


def preprocess_image(src_img, box_outline=True):
    """
    Take the image (a frame of video) and process it so other functions can do their job easier.
    """
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray_img, 127, 255, 0)
    blur_img = cv2.blur(thresh_img, (8, 8))
    contours, _ = cv2.findContours(blur_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = get_bounding_boxes(contours)
    if box_outline:
        for box in bounding_boxes:
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    return thresh_img, src_img


def get_truck_wall_code(src_img):
    """
    Take an pre-processed image, return the smaller image only contain the truck's container with code.
    Then applied perspective transformation to turn it into rectangle shape.
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
    cv2.resizeWindow('Frame', 1500, 500)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Only take every 10th frame
            if count % 10 == 0:
                prep_img, draw_img = preprocess_image(frame)
                prep_img = cv2.cvtColor(prep_img, cv2.COLOR_GRAY2RGB)
                stacked_img = np.hstack([prep_img, draw_img])
                cv2.imshow("Frame", stacked_img)

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

# TODO: Detect the biggest contour
# TODO: Classify is this a truck or not
# TODO: Find the truck side and perspective transform it
# TODO: Find the code
# TODO: OCR it
# TODO: Need to be fast enough to use real time?
