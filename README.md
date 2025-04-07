# Design and Implementation of an Automated Sorting System Using Mechatronics Principle
PROBLEM STATEMENT: 
  Design and Implementation of an Automated Sorting System Using Mechatronics Principle.
  
ABSTRACT: 
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
# Core Workflow:
1. IR sensor detects object → pauses conveyor belt  
2. Camera captures image → OpenCV processes (HSV conversion + masking)  
3. Dominant color identified → triggers servo action:  
   -->Blue: 150° (right bin)  
   -->Red: 45° (left bin)  
   -->Green: 90° (neutral/default bin)  
4. Conveyor resumes after 3-second delay

CIRCUIT DIAGRAM:

![WhatsApp Image 2025-04-07 at 15 16 36_66edf939](https://github.com/user-attachments/assets/d43fab53-dacd-45d1-ad5d-f2be14f21549)



   
