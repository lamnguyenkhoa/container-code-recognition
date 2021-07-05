import cv2


def display_image_cv2(img, window_name="output", scaling=True):
    if scaling:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        old_h, old_w = img.shape[0:2]
        new_h, new_w = old_h, old_w
        if old_w > old_h:
            while new_w < 400:
                new_w += old_w
                new_h += old_h
        else:
            while new_h < 400:
                new_w += old_w
                new_h += old_h
        cv2.resizeWindow(window_name, new_w, new_h)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
