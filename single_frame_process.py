import cv2
from src import ocr
import argparse
from src.code_region_detector import build_model, detect
from src.code_image_cleaner import process_image_for_ocr
from src.utils import display_image_cv2, resize_to_suitable


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


def limit_to_one(class_ids, boxes, confidences):
    class_id = None
    box = None
    confidences = None
    return


def get_code_and_draw(frame, class_ids, classes, boxes, debug=False):
    """
    Detect the code in the frame and annotate it.
    """
    n_obj = len(class_ids)
    codes = []
    # Crop the code part out and process it
    for i in range(n_obj):
        if classes[class_ids[i]] == "sidecode":
            print("single_frame_process/get_code_and_draw(): sidecode not working yet!")
            continue
        x, y, w, h = boxes[i]
        extra_pix = 2  # Get a bit bigger crop to make sure we cover everything
        crop_img = frame[round(y)-extra_pix:round(y+h)+extra_pix, round(x)-extra_pix:round(x+w)+extra_pix]
        print("single_frame_process/get_code_and_draw(): cropped image shape", crop_img.shape)
        if crop_img.shape[0] == 0 or crop_img.shape[1] == 0:
            continue
        crop_img = resize_to_suitable(crop_img)
        print("single_frame_process/get_code_and_draw(): resized image shape", crop_img.shape)
        if debug:
            display_image_cv2(crop_img, "cropped code image")
        clean_img = process_image_for_ocr(crop_img, debug)
        clean_img = cv2.bitwise_not(clean_img)
        clean_img = cv2.blur(clean_img, (2, 2))
        res = ocr.find_code_in_image(clean_img)
        print("Detected code:", res)
        codes.append(res)
        if debug:
            display_image_cv2(clean_img, "cleaned code image")
        write_result_on_image(frame, res, boxes[i])
    return frame, codes


def main(args):
    """
    If run this file, it will perform code region detection and OCR it on an image instead of a video.
    """
    src_img = cv2.imread(args['image'])
    # Build model and detect code region
    net, classes, output_layers = build_model(args['classes'], args['weights'], args['config'])
    # For some reason, enable CUDA make single image detect slower?
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    class_ids, boxes, confidences = detect(net, src_img, output_layers)
    src_img, _ = get_code_and_draw(src_img, class_ids, classes, boxes, debug=True)
    display_image_cv2(src_img, "final")
    cv2.imwrite("output.jpg", src_img)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    argument = argument_parser()
    main(argument)
