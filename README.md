# Design and Implementation of an Automated Sorting System Using Mechatronics Principle
Problem Statement:  
Design and Implementation of an Automated Sorting System Using Mechatronics Principle.
  
Abstract:  
This project implements an automated color-based object sorting system using a Raspberry Pi, stepper and servo motors, an IR sensor, and OpenCV for computer vision. The system detects objects on a conveyor belt via an IR sensor, captures their images, and processes them in real-time to identify colors (Red, Green, Blue). Based on the detected color, servo motors actuate to sort items into designated bins. The workflow integrates multi-threading for concurrent motor control and image processing, ensuring efficiency. Key technologies include Raspberry Pi GPIO, PWM-based servo control, HSV color masking, and contour detection. The system demonstrates embedded automation with applications in industrial sorting, recycling, and smart warehousing.
Keywords: Raspberry Pi, OpenCV, Stepper Motor, Servo Control, Color Detection, Automation.

Demonstration:  
https://youtu.be/bXQAf65EoB4

Documentation:  
https://docs.google.com/document/d/13cMJTbjL3LsCIIEnE3JMk_mNxjLzLZRmM-X0NAvaSHs/edit?usp=sharing 

✨ Features:

Real-time color detection (Red/Green/Blue) using OpenCV
IR sensor-triggered conveyor belt control
Servo-powered sorting mechanism with precise angle control
Multi-threaded Python code for smooth concurrent operation

⚙️ Software Architecture   
Core Workflow:
1. IR sensor detects object → pauses conveyor belt  
2. Camera captures image → OpenCV processes (HSV conversion + masking)  
3. Dominant color identified → triggers servo action:  
   -->Blue:  (right bin)  
   -->Red:  (left bin)  
   -->Green: (neutral/default bin)  
4. Conveyor resumes 






   
