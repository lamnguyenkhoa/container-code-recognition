# Object detection: detect the code region on image
import cv2
import numpy as np
import argparse


def argument_parser():
    # handle command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help='path to input image')
    ap.add_argument('-c', '--config', required=True, help='path to yolo config file')
    ap.add_argument('-w', '--weights', required=True, help='path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', required=True, help='path to text file containing class names')
    args = vars(ap.parse_args())
    return args


def get_output_layers(net):
    """ Function to get the output layer names in the architecture """
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, colors):
    """ function to draw bounding box on the detected object with class name """
    label = str(classes[class_id])
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def main(args):
    # read input image
    image = cv2.imread(args['image'])
    im_h, im_w = image.shape[0:2]
    scale = 0.00392
    # read class names from text file
    with open(args['classes'], 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    # generate different colors for different classes
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # read pre-trained model and config file to create the network
    net = cv2.dnn.readNet(args['weights'], args['config'])
    # create input blob to prepare image for the network
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # run inference through the network
    # and gather predictions from output layers
    outs = net.forward(get_output_layers(net))
    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    # for each detection from each output layer,
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
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
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    # go through the detections remaining after nms and draw bounding box
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y),
                          round(x+w), round(y+h), classes, colors)
    cv2.imshow("object detection", image)
    cv2.waitKey()
    cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # arguments = argument_parser()
    debug_arguments = {'image': 'images/dog.jpg', 'config': 'yolov3.cfg',
                       'weights': 'yolov3.weights', 'classes': 'yolov3.txt'}
    main(debug_arguments)
