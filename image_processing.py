import cv2
import numpy as np
from utils import display_image_cv2


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def is_contour_bad(c, src_img):
    im_h, im_w = src_img.shape[0:2]
    box = cv2.boundingRect(c)
    x, y, w, h = box[0], box[1], box[2], box[3]
    # If image is a back code (width larger than height)
    if im_w > im_h:
        if h >= 0.8*im_h:  # likely to be a bar
            print("found a bar contour")
            return True
        if x < 0.4*im_w and y > 0.6*im_h:  # lower left unrelated symbols
            print("found a unrelated contour")
            return True
        if w*h < 0.003*im_h*im_w:  # Noise w/ area < 0.5% of image's area
            print("found a tiny noise contour")
            return True
    # Else, it a side code
    else:
        if w*h < 0.001*im_h*im_w:  # Noise
            print("found a tiny noise contour")
            return True
        if x+w >= 0.5*im_w and y+h >= 0.4*im_h:
            print("found a unrelated contour")
            return True
    return False


def otsu_threshold(src_img):
    """ NOT expected to return white text on black background"""
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    # blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
    _, thresh_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh_img


def is_it_bbwt(thresh_img, depth=2):
    """ Make sure the thresh img has white text on black background """
    im_h, im_w = thresh_img.shape[0:2]
    # Calculate the pixel value of image border
    total_pixel_value = np.sum(thresh_img)
    center_img = thresh_img[depth:im_h-depth, depth:im_w-depth]
    center_pixel_value = np.sum(center_img)
    border_bw_value = (total_pixel_value - center_pixel_value) / (im_h*im_w - center_img.size)
    print("BBWT value:", border_bw_value)
    return border_bw_value > 127  # If True mean not bbwt, and thresh must be invert


def cleanup_backcode_image(src_img, visual=False):
    """
    Clean up other cluttering on the back code and return a threshold image.
    """
    print("Image shape:", src_img.shape)
    thresh = otsu_threshold(src_img)
    if is_it_bbwt(thresh):
        cv2.bitwise_not(thresh, thresh)  # invert
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.ones(src_img.shape[:2], dtype="uint8") * 255
    # loop over the contours
    # cv2.drawContours(src_img, cnts, -1, (0, 255, 0), 1)
    for c in cnts:
        # Draw contour for visualization
        if visual:
            box = cv2.boundingRect(c)
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=1)
        # if the contour is bad, draw it on the mask (to remove it later)
        if is_contour_bad(c, src_img):
            cv2.drawContours(mask, [c], -1, 0, -1)
    # remove the contours from the image and show the resulting images
    result = cv2.bitwise_and(thresh, thresh, mask=mask)
    if visual:
        display_image_cv2(src_img, "original w/ box")
        display_image_cv2(thresh, "thresh")
        display_image_cv2(result, "result")
    return result


def main():
    # Test threshold and cleanup ability
    src_img = cv2.imread("images/code4.png")
    clean_img = cleanup_backcode_image(src_img, True)


if __name__ == "__main__":
    main()
