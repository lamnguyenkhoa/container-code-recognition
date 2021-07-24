import cv2


def resize_to_suitable(img, min_dim=400):
    old_h, old_w = img.shape[0:2]
    if old_w == 0 or old_h == 0:
        return img
    new_h, new_w = old_h, old_w
    if old_w > old_h:
        while new_w < min_dim:
            new_w += old_w
            new_h += old_h
    else:
        while new_h < min_dim:
            new_w += old_w
            new_h += old_h
    resized = cv2.resize(img, (new_w, new_h), cv2.INTER_AREA)
    return resized


def display_image_cv2(img, window_name="output", scaling=True):
    if scaling:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        resized_img = resize_to_suitable(img)
        cv2.imshow(window_name, resized_img)
    else:
        cv2.imshow(window_name, img)
    cv2.waitKey(0)
