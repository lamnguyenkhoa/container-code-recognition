import cv2
import numpy as np
from src.utils import display_image_cv2


def rotate_image(thresh_img, debug=False):
    """ Rotate an image. Required input to be a binary image."""
    if debug:
        display_image_cv2(thresh_img, "prerotate")
    im_h, im_w = thresh_img.shape[0:2]
    if im_h > im_w:
        # Not yet implemented for vertical side code
        print("code_image_cleaner/rotate_image(): Not yet implemented for vertical side code")
        return thresh_img

    tmp = np.where(thresh_img > 0)
    row, col = tmp
    # note: column_stack is just vstack().T (aka transposed vstack)
    coords = np.column_stack((col, row))
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    if debug:
        box_points = cv2.boxPoints(rect)
        box_points = np.int0(box_points)
        debug_box_img = cv2.drawContours(thresh_img.copy(), [box_points], 0, (255, 255, 255), 2)
        display_image_cv2(debug_box_img, "debug box rotate", False)
    # the v4.5.1 `cv2.minAreaRect` function returns values in the
    # range (0, 90]); as the rectangle rotates clockwise the
    # returned angle approach 90.
    if angle > 45:
        # if angle > 45 it will rotate left 90 degree into vertical standing form, so rotate another 270 degree
        # will bring it back to good. Otherwise, it will rotate nice.
        angle = 270 + angle

    # rotate the image
    (h, w) = thresh_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(thresh_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
    print("code_image_cleaner/rotate_image(): rotated", angle)
    return rotated


def is_contour_bad(c, src_img):
    im_h, im_w = src_img.shape[0:2]
    box = cv2.boundingRect(c)
    x, y, w, h = box[0], box[1], box[2], box[3]
    # If image is a back code (width larger than height)
    if im_w > im_h:
        if h >= 0.6*im_h:  # likely to be a bar
            print("code_image_cleaner/is_contour_bad(): found a bar contour")
            return True
        if x < 0.4*im_w and y > 0.6*im_h:  # lower left unrelated symbols
            print("code_image_cleaner/is_contour_bad(): found a unrelated contour")
            return True
        if w*h < 0.002*im_h*im_w:  # Noise w/ area < 0.2% of image's area
            print("code_image_cleaner/is_contour_bad(): found a tiny noise contour")
            return True
        if x <= 1 or x >= (im_w-1) or y <= 1 or y >= (im_h-1):
            if w*h < 0.05*im_h*im_w:
                print(x, y, w, h, im_w, im_h)
                print("code_image_cleaner/is_contour_bad(): found a sus edge-touched small contour")
                return True
    # Else, it a side code
    else:
        if w*h < 0.001*im_h*im_w:  # Noise
            print("code_image_cleaner/is_contour_bad(): found a tiny noise contour")
            return True
        if x+w >= 0.5*im_w and y+h >= 0.4*im_h:
            print("code_image_cleaner/is_contour_bad(): found a unrelated contour")
            return True
    return False


def remove_noise(cnts, thresh, src_img, debug=False):
    print("===Start removing noise===")
    mask = np.ones(thresh.shape[:2], dtype="uint8") * 255
    # loop over the contours
    for c in cnts:
        # Draw contour for visualization
        if debug:
            box = cv2.boundingRect(c)
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=1)
        # if the contour is bad, draw it on the mask (to remove it later)
        if is_contour_bad(c, src_img):
            cv2.drawContours(mask, [c], -1, 0, -1)
    # remove the contours from the image and show the resulting images
    result = cv2.bitwise_and(thresh, thresh, mask=mask)
    print("=====Finish=====")
    return result


def otsu_threshold(src_img):
    """ NOT expected to return white text on black background"""
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    # blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
    _, thresh_img1 = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh_img2 = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 17)
    thresh_img = cv2.bitwise_and(thresh_img1, thresh_img2)
    return thresh_img


def make_sure_it_bbwt(thresh_img, depth=2):
    """ Make sure the thresh img has white text on black background """
    im_h, im_w = thresh_img.shape[0:2]
    # Calculate the pixel value of image border
    total_pixel_value = np.sum(thresh_img)
    center_img = thresh_img[depth:im_h-depth, depth:im_w-depth]
    center_pixel_value = np.sum(center_img)
    border_bw_value = (total_pixel_value - center_pixel_value) / (im_h*im_w - center_img.size)
    print("code_image_cleaner/is_it_bbwt():BBWT value:", border_bw_value)
    # If True mean it is not bbwt, and thresh must be invert
    if border_bw_value > 127:
        cv2.bitwise_not(thresh_img, thresh_img)


def process_image_for_ocr(src_img, debug=False):
    """
    Clean up other cluttering on the back code and return a binary image. Run this from other file.
    """
    # Binarization
    thresh = otsu_threshold(src_img)
    make_sure_it_bbwt(thresh)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Remove noise
    clean = remove_noise(cnts, thresh, src_img, debug)
    # Rotate
    rotated = rotate_image(clean, debug)
    if debug:
        display_image_cv2(src_img, "original w/ box")
        display_image_cv2(thresh, "thresh")
        display_image_cv2(clean, "removed noise")
        display_image_cv2(rotated, "rotated")
    return rotated


def main():
    """ Test threshold and cleanup ability """
    src_img = cv2.imread("../images/code3.png")
    clean_img = process_image_for_ocr(src_img, True)


if __name__ == "__main__":
    main()
