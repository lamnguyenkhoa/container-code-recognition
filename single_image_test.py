import cv2
import image_processing
import ocr
from utils import display_image_cv2


def get_code_in_image():
    """
    Detect the code in the image. Use in main program.
    """


def main():
    """
    Test recognition ability on a single image. Only used for testing
    """
    src_img = cv2.imread("images/code1.png")
    clean_img = image_processing.cleanup_backcode_image(src_img)
    clean_img = cv2.bitwise_not(clean_img)
    clean_img = cv2.blur(clean_img, (2, 2))
    res = ocr.find_code_in_image(clean_img)
    print(clean_img.shape)
    print(res)
    display_image_cv2(clean_img, "Final result")


if __name__ == "__main__":
    main()
