# Doctor Rag
================

## Project Overview
-----------------

Doctor Rag is an AI-powered music generation tool designed to create ragtime music compositions. This project utilizes advanced machine learning algorithms to generate unique and coherent musical pieces.

## Features
------------

*   **Music Generation**: The tool can generate ragtime music compositions with varying levels of complexity.
*   **Customization**: Users can input parameters to control the generated music, such as tempo, time signature, and melody complexity.
*   **Real-time Feedback**: The system provides real-time feedback on the generated music, allowing users to refine their input parameters.

## Tech Stack
-------------

*   **Programming Language**: Python 3.9+
*   **Machine Learning Framework**: TensorFlow 2.4+
*   **Music Library**: Music21 6.0+

## Architecture
-------------

### System Components

*   **Input Module**: Responsible for processing user input parameters and generating a musical composition.
*   **Music Generation Module**: Utilizes machine learning algorithms to generate ragtime music compositions based on user input.
*   **Output Module**: Responsible for rendering the generated music in a suitable format.

### System Flow

1.  **User Input**: The user inputs parameters for the music generation process.
2.  **Input Processing**: The input module processes the user input and generates a musical composition.
3.  **Music Generation**: The music generation module utilizes machine learning algorithms to generate the ragtime music composition.
4.  **Output Rendering**: The output module renders the generated music in a suitable format.

## Running the Project
----------------------

### Prerequisites

*   Install Python 3.9+
*   Install TensorFlow 2.4+
*   Install Music21 6.0+

### Running the Project

1.  Clone the repository: `git clone https://github.com/hammas-shahzad-shani/doctor_rag.git`
2.  Navigate to the project directory: `cd doctor_rag`
3.  Run the project: `python main.py`

### Example Usage

```bash
python main.py --tempo 120 --time_signature 4/4 --melody_complexity 0.5
```

This will generate a ragtime music composition with a tempo of 120 BPM, a time signature of 4/4, and a melody complexity of 0.5.