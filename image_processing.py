import cv2
import numpy as np
from utils import display_image_cv2


def get_bounding_boxes(contours, img_dim):
    bounding_boxes = []
    im_area = img_dim[0]*img_dim[1]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 0.0001*im_area or area > 0.8*im_area:  # Remove noise
            continue
        box = cv2.boundingRect(cnt)
        bounding_boxes.append(box)
    return bounding_boxes


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def is_contour_bad(c, src_img):
    im_h, im_w = src_img.shape[0:2]
    box = cv2.boundingRect(c)
    x, y, w, h = box[0], box[1], box[2], box[3]
    if h >= 0.8*im_h:  # likely to be a bar
        print("found a bar contour")
        return True
    if x < 0.4*im_w and y > 0.6*im_h:  # lower left unrelated symbols
        print("found a unrelated contour")
        return True
    if w*h < 0.001*im_h*im_w:  # Noise
        print("found a tiny noise contour")
        return True
    return False


def bbwt_threshold(src_img):
    """
    Turn image into binary color: Black Background White Text.
    Require original colored image.
    """
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    avg_color_per_row = np.average(gray_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    if avg_color > 127:
        print("This is a bright image")
        ret, thresh_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)
    else:
        print("This is a dark image")
        ret, thresh_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    return thresh_img


def cleanup_backcode_image(src_img, visual=False):
    """
    Clean up other cluttering on the back code and return a threshold image.
    """
    thresh = bbwt_threshold(src_img)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.ones(src_img.shape[:2], dtype="uint8") * 255
    # loop over the contours
    # cv2.drawContours(src_img, cnts, -1, (0, 255, 0), 1)
    print("Image shape:", src_img.shape)
    for c in cnts:
        box = cv2.boundingRect(c)
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=1)
        # if the contour is bad, draw it on the mask
        if is_contour_bad(c, src_img):
            cv2.drawContours(mask, [c], -1, 0, -1)
    # remove the contours from the image and show the resulting images
    result = cv2.bitwise_and(thresh, thresh, mask=mask)
    if visual:
        display_image_cv2(src_img, "original")
        display_image_cv2(thresh, "thresh")
        display_image_cv2(mask, "mask")
        display_image_cv2(result, "result")
    return result


def main():
    # Test cleanup ability
    src_img = cv2.imread("images/code2.png")
    clean_img = cleanup_backcode_image(src_img)
    display_image_cv2(clean_img, "result", False)


if __name__ == "__main__":
    main()
