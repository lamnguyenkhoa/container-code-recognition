import cv2
import argparse
import numpy as np
from code_region_detector import build_model, detect
from single_frame_process import get_code_and_draw


def argument_parser():
    """ Handle command line arguments """
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--video', default='videos/video1.mp4', help='path to input video')
    ap.add_argument('-c', '--config', default='yolov4.cfg', help='path to yolo config file')
    ap.add_argument('-w', '--weights', default='yolov4.weights', help='path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', default='yolov4.txt', help='path to text file containing class names')
    args = vars(ap.parse_args())
    return args


def main(args):
    cap = cv2.VideoCapture(args['video'])
    if not cap.isOpened():
        print("truck_code_ocr/main(): Error opening video stream or file")

    # Read until video is completed
    cv2.namedWindow('Output frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Output frame', 1500, 800)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Only take every 4th frame
            if count % 4 == 0:
                # Detect code and recognize it here
                net, classes = build_model(args['classes'], args['weights'], args['config'])
                class_ids, boxes, _ = detect(net, frame)
                frame, codes = get_code_and_draw(frame, class_ids, classes, boxes)
                cv2.imshow("Output frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(10) and 0xFF == ord('q'):
                break
            count += 1
        else:
            break
    # When everything done, release the video capture object
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)
