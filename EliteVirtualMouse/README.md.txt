# Elite Virtual Mouse System

This is a hands-free virtual mouse system that uses hand gestures, tracked by a webcam, to control the mouse cursor. It features click detection, right-click, and scrolling gestures, built using Python, OpenCV, Mediapipe, and PyAutoGUI libraries.

## Features:
- **Cursor Movement:** Controlled by the index finger.
- **Clicking:** Left-click by pinching the thumb and index finger.
- **Right-Click:** Hold a pinch between the index and thumb.
- **Scrolling:** Controlled by the distance between the index and middle fingers.
- **Deadzone:** Prevents unintended cursor movement near the center of the screen.

## Requirements:
- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI
- Numpy

## Setup:
1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Elite_Virtual_Mouse_System.git
    cd Elite_Virtual_Mouse_System
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the program:

    ```bash
    python elite_virtual_mouse.py
    ```

## License:
This project is open-source and licensed under the MIT License.

