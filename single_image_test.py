import cv2
import image_processing
import ocr
from utils import display_image_cv2


def get_code_in_image():
    """
    Detect the code in the image. Use in main program.
    """


def resize_to_suitable(src_img):
    im_h, im_w = src_img.shape[0:2]
    resized_img = cv2.resize(src_img, 2)
    return resized_img


def main():
    """
    Test recognition ability on a single image. Only used for testing
    """
    src_img = cv2.imread("images/code2.png")
    clean_img = image_processing.process_image_for_ocr(src_img)
    clean_img = cv2.bitwise_not(clean_img)
    clean_img = cv2.blur(clean_img, (2, 2))
    res = ocr.find_code_in_image(clean_img)
    print(res)
    display_image_cv2(clean_img, "Final result")


if __name__ == "__main__":
    main()

# TODO: Find a wat to deskew vertical code
# TODO: But for now, focus on trying to make it run just based on back code
