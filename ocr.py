import pytesseract


def build_tesseract_options(is_sidecode=False):
    # tell Tesseract to only OCR alphanumeric characters
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if is_sidecode:
        options = "--psm 6"  # Assume a single uniform block of text
    else:
        options = "--psm 3"  # Fully automatic page segmentation, but no OSD. (Default)
    options += " --oem 3"
    options += " -c tessedit_char_whitelist={}".format(alphanumeric)
    options += " load_freq_dawg=false load_system_dawg=false"  # Tesseract won't use dictionary
    # set the PSM mode
    # options += " --psm {}".format(7)
    # return the built options string
    return options


def error_check(original_code):
    ...


def reformat(original_code):
    """ Reformat the text into better format"""
    ...


def find_code_in_image(img):
    im_h, im_w = img.shape[0:2]
    if im_h > im_w:  # If this image is a side code image
        options = build_tesseract_options(True)
    else:
        options = build_tesseract_options(False)
    result = pytesseract.image_to_string(img, config=options)
    return result


def main():
    ...


if __name__ == '__main__':
    main()

