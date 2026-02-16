# 2022 Autonomous Field Robot

This repository contains the codebase for an entry in the **2022 Campus Autonomous Field Robot Competition**. The project integrates computer vision, Arduino-based hardware control, and serial communication to perform autonomous navigation and manipulation tasks, such as path following, color sign recognition, and fruit identification in agricultural environments.

## 🚀 Key Features

* **Integrated Control System**: A multi-layered architecture connecting a high-level Python controller with low-level Arduino firmware.
* **Computer Vision Modules**:
* **Color Sign Recognition**: Real-time detection and classification of field markers using OpenCV.
* **Fruit Identification**: Image-based logic to locate and recognize specific agricultural products.


* **Robust Serial Communication**: Reliable data exchange between PC (Ubuntu) and Arduino via `pyserial`, utilizing custom helper functions for motor and sensor control.
* **Version-Controlled Development**: Evolution of logic from initial drafts (`Main_v6`) to the fully integrated production version (`Main_v10_Final`).
* **Hardware Utility Suite**: Scripts for sensor calibration, camera testing, and modular hardware tests (Servos, Relays, RGB LEDs, Irrigation).

## 🛠️ Tech Stack & Tools

* **Programming Languages**: Python (Logic/Vision), C/C++ (Arduino Firmware)
* **Image Processing**: `OpenCV`, `NumPy`
* **Communication**: `pyserial` (UART protocol)
* **Development Environment**: Ubuntu Linux, Arduino IDE

## 📂 Repository Structure

* `Main/`: Core logic and versioned iterations (`v6`~`v9`). Includes vision modules: `color_sign_recog.py` and `fruit_recog.py`.
* `Main_v10_Final/`: The production-ready version containing `Main_Final.py` and the corresponding firmware `Main_v10_Final.ino`.
* `Integrated_Test/`: Test suites for system integration, including specific sign recognition tests (`Sign_IT.py`).
* `Tool/`: Utility scripts for data collection (e.g., `takePictures.py`) and image preprocessing.
* `Tracking/`: Arduino sketches and drafts specifically for the mobile tracking base.
* `Test/`: Unit tests for individual hardware components (Servo, Relay, Irrigation system).


## 📊 Project Outcomes

* **Accomplishments**: Successful integration of serial communication, reliable color sign detection, and modularized firmware samples.
* **Future Improvements**: Optimization of recognition algorithms for varied lighting conditions and PID tuning for smoother motion control.
