import pytesseract


def error_check(formatted_code):
    """ Assume code is using BIC container code format. """
    fixed_code = list(formatted_code)
    n = len(fixed_code)
    if n != 15:
        print("Code is not complete!")
    else:
        # First 4 characters are always letters
        for i in range(4):
            if fixed_code[i] == '1':
                fixed_code[i] = 'I'
            if fixed_code[i] == '4':
                fixed_code[i] = 'A'
            if fixed_code[i] == '6':
                fixed_code[i] = 'G'
            if fixed_code[i] == '8':
                fixed_code[i] = 'B'
        # The next 5 characters are always digits
        for i in range(4, 9):
            if fixed_code[i] == 'I':
                fixed_code[i] = '1'
            if fixed_code[i] == 'A':
                fixed_code[i] = '4'
            if fixed_code[i] == 'G':
                fixed_code[i] = '6'
            if fixed_code[i] == 'B':
                fixed_code[i] = '8'
        # This character is always letters (can only be G, R, U, P or T)
        if fixed_code[13] == '6':
            fixed_code[13] = 'G'
        # The following characters is usually 1
        if fixed_code[14] == 'I' or fixed_code[14] == '1':
            fixed_code[14] = '1'
        else:
            print("Bad images or it isn't BIC code")
            print("Character 15th detected as", fixed_code[14], "and has been fixed.")
            fixed_code[14] = '1'
    fixed_code = "".join(fixed_code)
    return fixed_code


def reformat_code(original_code):
    """ Reformat the text into better format. Format assumed to be BIC container code. """
    formatted_code = None
    n = len(original_code)
    if n <= 20:
        # Likely to be backcode
        formatted_code = original_code[0:n - 1]  # Remove weird last character
        formatted_code = formatted_code.replace(" ", "")  # Remove whitespace characters
        formatted_code = formatted_code.replace("\n", "")  # Remove whitespace character
    else:
        # Side code, very prone to error
        print("ocr/reformat_code: Sidecode not implemented!")
        return original_code
        # tmp = original_code[0:n-1]  # Remove weird last character
        # tmp = tmp.replace(" ", "")  # Remove whitespace characters
        # tmp = tmp.replace("\n", "")  # Remove whitespace character
        # owner_code = tmp[0]+tmp[2]+tmp[4]+tmp[6]
        # iso_code = tmp[1]+tmp[3]+tmp[5]+tmp[7]
        # serial_number = tmp[8:-2]  # From 9th digit to 2nd last digit
        # check_digit = tmp[-1]  # Last digit
        # formatted_code = owner_code + serial_number + check_digit + iso_code
    return formatted_code


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


def find_code_in_image(img):
    im_h, im_w = img.shape[0:2]
    if im_h > im_w:  # If this image is a side code image
        options = build_tesseract_options(True)
    else:
        options = build_tesseract_options(False)
    result = pytesseract.image_to_string(img, config=options)
    result = reformat_code(result)
    result = error_check(result)
    return result


def main():
    ...


if __name__ == '__main__':
    main()

# TODO: Improve reformat for side code
# TODO: Use ISO_6346 check digits for better accuracy
# https://en.wikipedia.org/wiki/ISO_6346#Check_digit
# https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/iso6346.py
