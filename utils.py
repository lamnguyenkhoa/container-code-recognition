import cv2


def display_image_cv2(img, window_name="output", fixed_size=True):
    if fixed_size:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 400, 400)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)