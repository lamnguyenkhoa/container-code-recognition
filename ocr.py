import pytesseract


def build_tesseract_options(is_backcode):
    # tell Tesseract to only OCR alphanumeric characters
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    options = "-c tessedit_char_whitelist={}".format(alphanumeric)
    # set the PSM mode
    # options += " --psm {}".format(7)
    # return the built options string
    return options


def error_check(original_code):
    ...


def reformat(original_code):
    """ Reformat the text into better format"""
    ...


def find_code_in_image(img, is_backcode=True):
    options = build_tesseract_options(is_backcode)
    result = pytesseract.image_to_string(img, config=options)
    return result


def main():
    ...


if __name__ == '__main__':
    main()

