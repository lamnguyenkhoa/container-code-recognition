import cv2
import argparse

from single_frame_process import get_code_and_draw
from src.code_region_detector import build_model, detect, draw_all_bounding_boxes


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

    # Load the model
    net, classes, output_layers = build_model(args['classes'], args['weights'], args['config'])
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    # Read until video is completed
    cv2.namedWindow('Output frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Output frame', 1280, 720)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Only take every 2nd frame
            if count % 2 == 0:
                # Detect code and recognize it here
                class_ids, boxes, confidences = detect(net, frame, output_layers)
                # draw_all_bounding_boxes(frame, boxes, class_ids, confidences, classes)
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
