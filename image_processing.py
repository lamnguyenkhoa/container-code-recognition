import cv2


def get_bounding_boxes(contours, img_dim):
    """
    Transform contours into list of bounding boxes. Also remove some noise contours.
    """
    bounding_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        box = cv2.boundingRect(cnt)
        if area > 0.1*img_dim[0]*img_dim[1] \
                or area < 100:
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
    bounding_boxes = get_bounding_boxes(contours, src_img.shape)
    if box_outline:
        for box in bounding_boxes:
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    return thresh_img, src_img


def main():
    """
    Test other functions
    """
    ...


if __name__ == "__main__":
    main()
