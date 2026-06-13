# Teachable Machine
=====================

### Project Overview

Teachable Machine is an open-source project that enables the conversion of machine learning models into a format that can be easily deployed on edge devices, such as mobile phones or embedded systems. This project utilizes the TensorFlow.js library to export Keras models into a format that can be executed on the web or on edge devices.

### Features

*   **Model Export**: Export Keras models into a format that can be executed on the web or on edge devices using TensorFlow.js.
*   **Edge Deployment**: Deploy machine learning models on edge devices, such as mobile phones or embedded systems.
*   **Cross-Platform Compatibility**: Compatible with a wide range of platforms, including web, mobile, and embedded systems.

### Tech Stack

*   **Programming Language**: Python
*   **Machine Learning Framework**: TensorFlow, Keras
*   **Model Export Library**: TensorFlow.js
*   **Containerization**: Docker

### Architecture

The Teachable Machine project consists of the following components:

*   **Model Export**: The model export component is responsible for converting Keras models into a format that can be executed on the web or on edge devices using TensorFlow.js.
*   **Dockerization**: The Dockerfile is used to containerize the project, ensuring that the environment and dependencies are consistent across different platforms.
*   **Testing**: The `test_keras_export.py` file contains unit tests to ensure that the model export functionality is working correctly.

### Setup and Installation

To set up and install the project, follow these steps:

1.  Clone the repository using `git clone https://github.com/hammas-shahzad-shani/teachable-machine.git`
2.  Install the required dependencies by running `pip install -r requirements.txt`
3.  Build the Docker image by running `docker build -t teachable-machine .`
4.  Run the Docker container by running `docker run -p 8080:8080 teachable-machine`

### Contributing

Contributions to the project are welcome. To contribute, please fork the repository and submit a pull request with your changes.

### License

The Teachable Machine project is licensed under the MIT License.

### Acknowledgments

The Teachable Machine project is built on top of the TensorFlow.js library and utilizes the Keras framework. We would like to thank the TensorFlow.js and Keras communities for their contributions to the project.

### Contact

For any questions or feedback, please contact Hammas Shahzad Shani at [hammas.shahzad.shani@gmail.com](mailto:hammas.shahzad.shani@gmail.com)