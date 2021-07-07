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


def reformat_code(original_code):
    """ Reformat the text into better format"""
    formatted_code = None
    n = len(original_code)
    if n <= 20:
        # Likely to be backcode
        formatted_code = original_code[0:n-1]  # Remove weird last character
        formatted_code = formatted_code.replace(" ", "")  # Remove whitespace characters
        formatted_code = formatted_code.replace("\n", "")  # Remove whitespace character
    else:
        # Side code, very prone to error
        tmp = original_code[0:n-1]  # Remove weird last character
        tmp = tmp.replace(" ", "")  # Remove whitespace characters
        tmp = tmp.replace("\n", "")  # Remove whitespace character
        owner_code = tmp[0]+tmp[2]+tmp[4]+tmp[6]
        iso_code = tmp[1]+tmp[3]+tmp[5]+tmp[7]
        serial_number = tmp[8:-2]  # From 9th digit to 2nd last digit
        check_digit = tmp[-1]  # Last digit
        formatted_code = owner_code + serial_number + check_digit + iso_code
    return formatted_code


def find_code_in_image(img):
    im_h, im_w = img.shape[0:2]
    if im_h > im_w:  # If this image is a side code image
        options = build_tesseract_options(True)
    else:
        options = build_tesseract_options(False)
    result = pytesseract.image_to_string(img, config=options)
    result = reformat_code(result)
    return result


def main():
    ...


if __name__ == '__main__':
    main()

# TODO: Improve reformat for side code
