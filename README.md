# Design and Implementation of an Automated Sorting System Using Mechatronics Principle
**Problem Statement:**   
Design and Implementation of an Automated Sorting System Using Mechatronics Principle.
  
**Abstract:**   
This project implements an automated color-based object sorting system using a Raspberry Pi, stepper and servo motors, an IR sensor, and OpenCV for computer vision. The system detects objects on a conveyor belt via an IR sensor, captures their images, and processes them in real-time to identify colors (Red, Green, Blue). Based on the detected color, servo motors actuate to sort items into designated bins. The workflow integrates multi-threading for concurrent motor control and image processing, ensuring efficiency. Key technologies include Raspberry Pi GPIO, PWM-based servo control, HSV color masking, and contour detection. The system demonstrates embedded automation with applications in industrial sorting, recycling, and smart warehousing.
Keywords: Raspberry Pi, OpenCV, Stepper Motor, Servo Control, Color Detection, Automation.

**Demonstration:**  
https://youtu.be/bXQAf65EoB4

**Documentation:**  
https://docs.google.com/document/d/13cMJTbjL3LsCIIEnE3JMk_mNxjLzLZRmM-X0NAvaSHs/edit?usp=sharing 

**✨ Features:**

Real-time color detection (Red/Green/Blue) using OpenCV
IR sensor-triggered conveyor belt control
Servo-powered sorting mechanism with precise angle control
Multi-threaded Python code for smooth concurrent operation

 
**Core Workflow:**
1. IR sensor detects object → pauses conveyor belt  
2. Camera captures image → OpenCV processes (HSV conversion + masking)  
3. Dominant color identified → triggers servo action:  
   -->Blue:  (right bin)  
   -->Red:  (left bin)  
   -->Green: (neutral/default bin)  
4. Conveyor resumes

**System Architecture:**

![image](https://github.com/user-attachments/assets/ebb6e9d1-d788-41a0-ac6b-1c5646534893)

**Setup Instructions:**
Step 1: Clone the Repository
```
git clone https://github.com/epsibamiriam/Automated-Sorting-System-Using-Mechatronics-Principles.git
cd Automated-Sorting-System-Using-Mechatronics-Principles
```
Step 2: Set Up Python Environment
```
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```
Step 3: Hardware Connections

Refer to the documentation for the connections
https://docs.google.com/document/d/13cMJTbjL3LsCIIEnE3JMk_mNxjLzLZRmM-X0NAvaSHs/edit?usp=sharing

Step 4: Test Camera
```
# Verify camera detection
lsusb | grep "Intel"  # For Intel camera
# OR
libcamera-hello       # For Raspberry Pi Camera
```
Step 5: Run the System
```
python3 sorting_system.py
```

Step 6: Access Web Interface
```
http://<your-pi-ip>:5000
```
**Troubleshooting:**

Camera not detected?
Check USB connection or run v4l2-ctl --list-devices
GPIO errors?
Ensure RPi.GPIO is installed (pip install RPi.GPIO)
Web interface blank?
Verify Flask/SocketIO logs for errors


   
