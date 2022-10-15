# Container Code Recognition

**Status: Dropped**

This project will take a video or an image and used YOLOv4 Object detection
to detect the container codes (on the back or side of the container) and used OCR to read it into text.

The project is just a tech demo in disguise and its performance is questionable. It's best suited to just explore it for educational purpose. Feel free to contact me and ask questions.

Plan for improvement:

- Train a better YOLO model.
- Improve the OCR function.

If installed opencv with CUDA-enabled, the program will run faster. It still run
without CUDA/GPU, but slower, take ~0.5 second for an image.

## How to run

To run on a single image, use command:

`python single_frame_process -i path\to\img -c path\to\config
-w path\to\weights -cl path\to\classname`

Example: `python single_frame_process -i images\container1.png -c yolov4.cfg
-w yolov4.weights -cl yolov4.txt`

To run on a video, use command:

`python truck_code_ocr -v path\to\video -c path\to\config
-w path\to\weights -cl path\to\classname`

Note: If not given arguments, they will take the default value, which is
demo_input.jpg for -i, videos/video1.mp4 for -v and yolov4.* file for -c, -w and -cl.

## Required file

The .weights file is not included in repo because it has large size (~250mb).
Download the yolov4.weights file here and put it in the root folder:

The current .weights file is very low-quality, trained on 20 train images
and 4 test images with 1000 iterations using darknet.

<https://drive.google.com/file/d/18VLouk68J13xmc_AVwiKE8nIRUAFnl5T/view?usp=sharing>

## Example output

![Output example](./output.jpg?raw=true "Output example")
