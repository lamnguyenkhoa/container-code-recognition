import cv2
import numpy as np


def display_image_cv2(img, window_name="output"):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 400, 400)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)


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


def rotate_text(src_img):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    display_image_cv2(thresh)
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special caxse we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle
    # rotate the image to deskew it
    (h, w) = src_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(src_img, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    display_image_cv2(rotated)


def is_contour_bad(c, src_img):
    im_h, im_w = src_img.shape[0:2]
    box = cv2.boundingRect(c)
    x, y, w, h = box[0], box[1], box[2], box[3]
    if h >= 0.8*im_h:  # likely to be middle bar
        return True
    if x < 0.4*im_w and y > 0.6*im_h:  # lower left unrelated symbols
        return True
    return False


def cleanup_image(src_img):
    """
    Clean up other cluttering on the back code and return a threshold image.
    """
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    display_image_cv2(src_img, "original")
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.ones(src_img.shape[:2], dtype="uint8") * 255
    # loop over the contours
    # cv2.drawContours(src_img, cnts, -1, (0, 255, 0), 1)
    print(src_img.shape)
    for c in cnts:
        box = cv2.boundingRect(c)
        x, y, w, h = box[0], box[1], box[2], box[3]
        #print(x, y, w, h)
        cv2.rectangle(src_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=1)
        # if the contour is bad, draw it on the mask
        if is_contour_bad(c, src_img):
            print("found a bad contour")
            cv2.drawContours(mask, [c], -1, 0, -1)
    # remove the contours from the image and show the resulting images
    result = cv2.bitwise_and(thresh, thresh, mask=mask)
    display_image_cv2(thresh, "thresh")
    display_image_cv2(mask, "mask")
    display_image_cv2(result, "result")
    return thresh


def main():
    src_img = cv2.imread("images/code1.png")
    cleanup_image(src_img)


if __name__ == "__main__":
    main()
