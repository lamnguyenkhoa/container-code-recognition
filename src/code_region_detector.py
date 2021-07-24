# Object detection: detect the code region on image
import cv2
import numpy as np
import time


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes):
    """ Function to draw bounding box on the detected object with class name """
    label = str(classes[class_id])
    label = "%s : %f" % (label, confidence)
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
    color = COLORS[int(class_id) % len(COLORS)]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def draw_all_bounding_boxes(frame, boxes, class_ids, confidences, classes):
    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        draw_bounding_box(frame, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h), classes)


def build_model(classes_path='yolov4.txt', weights_path='yolov4.weights', config_path='yolov4.cfg'):
    # read class names from text file
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # read pre-trained model and config file to create the network
    print("code_region_detector/build_model(): loading YOLO from disk...")
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()  # Ex: conv_25, bn_25, relu_25, conv_26 ... yolo_106
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  # Get the yolo layer
    return net, classes, output_layers


def detect(net, frame, output_layers):
    """
    Return class id, confidence scores and bounding boxes for detected object (after NMS).
    This function is the same as using following built-in opencv functions:

    model = cv2.dnn_DetectionModel(net);
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True);
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    """
    # initialization
    class_ids = []
    confidences = []
    boxes = []
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.4
    scale = 1/255
    size = (320, 320)
    # create input blob to prepare image for the network
    blob = cv2.dnn.blobFromImage(frame, scalefactor=scale, size=size, mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    im_h, im_w = frame.shape[0:2]
    # run inference through the network and gather predictions from output layers
    start = time.time()
    outs = net.forward(output_layers)
    end = time.time()
    print("code_region_detector/detect(): YOLOv4 took {:.6f} seconds".format(end - start))

    # for each detection from each output layer, get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # convert yolo coords to opencv coords
                center_x = int(detection[0] * im_w)
                center_y = int(detection[1] * im_h)
                w = int(detection[2] * im_w)
                h = int(detection[3] * im_h)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    # clean up
    clean_class_ids = []
    clean_confidences = []
    clean_boxes = []
    for i in indices:
        j = i[0]
        clean_class_ids.append(class_ids[j])
        clean_boxes.append(boxes[j])
        clean_confidences.append(confidences[j])
    return clean_class_ids, clean_boxes, clean_confidences


def main():
    """ Used for testing """
    image = cv2.imread('../images/container1.png')
    net, classes, output_layers = build_model()

    # get NMS-ed result from detection
    class_ids, boxes, confidences = detect(net, image, output_layers)

    # draw it on the image
    draw_all_bounding_boxes(image, boxes, class_ids, confidences, classes)

    cv2.imshow("object detection", image)
    cv2.waitKey()
    cv2.imwrite("object_detection.jpg", image)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
