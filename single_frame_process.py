import cv2
import ocr
import argparse
from code_region_detector import build_model, detect
from code_image_cleaner import process_image_for_ocr
from utils import display_image_cv2, resize_to_suitable


def argument_parser():
    """ Handle command line arguments """
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', default='demo_input.jpg', help='path to input image')
    ap.add_argument('-c', '--config', default='yolov4.cfg', help='path to yolo config file')
    ap.add_argument('-w', '--weights', default='yolov4.weights', help='path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', default='yolov4.txt', help='path to text file containing class names')
    args = vars(ap.parse_args())
    return args


def write_result_on_image(src_img, res, box):
    x, y, w, h = box
    color = (255, 255, 0)
    cv2.rectangle(src_img, (round(x), round(y)), (round(x+w), round(y+h)), color, 2)
    cv2.putText(src_img, res, (round(x) - 10, round(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


def get_code_in_image(frame):
    """
    Detect the code in the image and write it on the frame. Use in main program.
    """
    annotated_frame = None
    codes = []
    return annotated_frame, codes


def main(args):
    """
    If run this file, it will perform code region detection and OCR it on an image instead of a video.
    """
    src_img = cv2.imread(args['image'])

    # Build model and detect code region
    net, classes = build_model(args['classes'], args['weights'], args['config'])
    class_ids, boxes, confidences = detect(net, src_img)
    n_obj = len(class_ids)
    # Crop the code part out and process it
    for i in range(n_obj):
        if classes[class_ids[i]] == "sidecode":
            print("single_frame_process/main(): sidecode not working yet!")
            continue
        x, y, w, h = boxes[i]
        crop_img = src_img[round(y):round(y+h), round(x):round(x+w)]
        print("single_frame_process/main(): cropped image shape", crop_img.shape)
        crop_img = resize_to_suitable(crop_img)
        print("single_frame_process/main(): resized image shape", crop_img.shape)
        display_image_cv2(crop_img, "cropped code image")
        clean_img = process_image_for_ocr(crop_img)
        clean_img = cv2.bitwise_not(clean_img)
        clean_img = cv2.blur(clean_img, (2, 2))
        res = ocr.find_code_in_image(clean_img)
        print(res)
        display_image_cv2(clean_img, "cleaned code image")
        write_result_on_image(src_img, res, boxes[i])
        display_image_cv2(src_img, "final")
        cv2.imwrite("output.jpg", src_img)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    argument = argument_parser()
    main(argument)