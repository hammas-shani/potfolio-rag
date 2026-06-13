# School-Uniform-Detection-using-yolo
## Project Overview

This repository contains a Jupyter Notebook-based implementation of a school uniform detection system using the YOLO (You Only Look Once) object detection algorithm. The system is designed to detect and classify school uniforms in images.

## Features

- **Object Detection**: The system uses YOLOv5 to detect school uniforms in images.
- **Custom Data Training**: The repository includes a Jupyter Notebook (`train_yolov5_object_detection_on_custom_data.ipynb`) that trains the YOLOv5 model on a custom dataset of school uniform images.
- **Image Processing**: The system includes a utility to merge images (`MergedImages.png`) for visualization purposes.

## Tech Stack

- **Programming Language**: Python 3.x
- **Deep Learning Framework**: PyTorch
- **Object Detection Algorithm**: YOLOv5
- **Jupyter Notebook**: For interactive development and experimentation

## Architecture

The system consists of two main components:

1. **Data Preparation**: The `train_yolov5_object_detection_on_custom_data.ipynb` notebook prepares the custom dataset for training the YOLOv5 model.
2. **Object Detection**: The `YOLO11_Uniform_Detection.ipynb` notebook uses the trained YOLOv5 model to detect school uniforms in images.

### Dependencies

- `torch`
- `torchvision`
- `yolov5`
- `matplotlib`
- `pandas`

### Usage

1. Clone the repository: `git clone https://github.com/hammas-shahzad-shani/School-Uniform-Detection-using-yolo.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the `train_yolov5_object_detection_on_custom_data.ipynb` notebook to train the YOLOv5 model on the custom dataset.
4. Run the `YOLO11_Uniform_Detection.ipynb` notebook to detect school uniforms in images.

### Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.