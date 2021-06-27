import cv2
import pytesseract


def separate_back_code(src_img):
    """
    Separate image of a container's back code into 2 smaller part to remove big noise.
    """
    # First, we detect the middle "bar"
    im_h = src_img.shape[0]
    bar_x = None
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        box = cv2.boundingRect(cnt)
        x, y, w, h = box[0], box[1], box[2], box[3]
        if h >= 0.9*im_h:  # This contour has box that is ~90% of image height
            bar_x = x
            break
    # Then we divide it
    left_part = src_img[:, 0:bar_x]
    right_part = src_img[:, bar_x+1:]
    return left_part, right_part


def main():
    pytesseract.pytesseract.tesseract_cmd = r'E:\miniconda3_venvs\TruckCodeRecognition\Library\bin\tesseract.exe'
    src_img = cv2.imread("images/code1.png")
    print(src_img.shape)
    lp, rp = separate_back_code(src_img)
    cv2.imshow('frame', lp)
    cv2.waitKey(0)
    print(pytesseract.image_to_string(lp))
    cv2.imshow('frame', rp)
    cv2.waitKey(0)
    print(pytesseract.image_to_string(rp))


if __name__ == '__main__':
    main()

