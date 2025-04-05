import RPi.GPIO as GPIO
import time
import threading
import cv2
import numpy as np
import os
from web_interface import system_data, socketio

# Set headless mode for OpenCV
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['DISPLAY'] = ':0'  # Fallback display setting

print("Waiting for 7 seconds before starting the system...")
time.sleep(7)

# Pin Configuration
MOTOR_PINS_1 = [5, 6, 13, 19]  # Stepper Motor 1 (BCM numbering)
MOTOR_PINS_2 = [20, 21, 26, 16]  # Stepper Motor 2 (BCM numbering)
IR_SENSOR_PIN_1 = 23           # IR Sensor 1 (BCM numbering)
SERVO_PIN_1 = 17               # Servo Motor 1 (BCM numbering)
SERVO_PIN_2 = 25               # Servo Motor 2 (BCM numbering)

# Stepper Motor Sequence (Fast Mode)
STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Define HSV color ranges for red, green, and blue
color_ranges = {
    "Red": [(0, 120, 70), (10, 255, 255)],  # Red lower range
    "Green": [(36, 50, 70), (89, 255, 255)],  # Green range
    "Blue": [(90, 50, 70), (128, 255, 255)]  # Blue range
}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(MOTOR_PINS_1, GPIO.OUT)
GPIO.setup(MOTOR_PINS_2, GPIO.OUT)
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)

# Motor Control Variables
motor_running = True
step_delay = 0.001  # Fast operation

# Servo Control
servo_1 = GPIO.PWM(SERVO_PIN_1, 50)  # 50Hz PWM frequency
servo_1.start(0)  # Initial position
servo_2 = GPIO.PWM(SERVO_PIN_2, 50)  # 50Hz PWM frequency
servo_2.start(0)  # Initial position

# Color count tracking
color_totals = {"Red": 0, "Green": 0, "Blue": 0}

def set_servo_angle(servo, angle, servo_name):
    duty_cycle = 2.5 + (angle / 18.0)
    log_entry = f"{time.strftime('%H:%M:%S')} - Setting {servo_name} to {angle} degrees"
    system_data['logs'].append(log_entry)
    socketio.emit('update_logs', log_entry)
    print(log_entry)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def run_stepper(motor_pins, reverse=False):
    global motor_running
    step_index = 0
    while True:
        if motor_running:
            step = STEP_SEQUENCE[step_index]
            if reverse:
                step = step[::-1]
            for i in range(4):
                GPIO.output(motor_pins[i], step[i])
            time.sleep(step_delay)
            step_index = (step_index + 1) % len(STEP_SEQUENCE)
        else:
            GPIO.output(motor_pins, GPIO.LOW)
            time.sleep(0.1)

def monitor_ir_sensor():
    global motor_running
    while True:
        if GPIO.input(IR_SENSOR_PIN_1) == GPIO.LOW:
            log_entry = f"{time.strftime('%H:%M:%S')} - Object detected! Stopping motors."
            system_data['logs'].append(log_entry)
            socketio.emit('update_logs', log_entry)
            print(log_entry)
            motor_running = False
            color = get_detected_color()
            handle_detected_color(color)
            time.sleep(3)
            motor_running = True
            log_entry = f"{time.strftime('%H:%M:%S')} - Restarting motors after 3 seconds pause."
            system_data['logs'].append(log_entry)
            socketio.emit('update_logs', log_entry)
            print(log_entry)
            time.sleep(10)
            set_servo_angle(servo_1, 90, "Servo 1")
            set_servo_angle(servo_2, 90, "Servo 2")
            log_entry = f"{time.strftime('%H:%M:%S')} - Servos reset to 90 degrees after 10 seconds total pause."
            system_data['logs'].append(log_entry)
            socketio.emit('update_logs', log_entry)
            print(log_entry)
        time.sleep(0.1)

def get_detected_color():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        error_msg = f"{time.strftime('%H:%M:%S')} - Error: Could not open camera."
        system_data['logs'].append(error_msg)
        socketio.emit('update_logs', error_msg)
        print(error_msg)
        return None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
                
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color_counts = {"Red": 0, "Green": 0, "Blue": 0}

            for color_name, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 500:
                        color_counts[color_name] += 1

            # Update web interface with current detection counts
            system_data['color_counts'] = color_counts
            socketio.emit('update_counts', {
                'current_red': color_counts["Red"],
                'current_green': color_counts["Green"],
                'current_blue': color_counts["Blue"],
                'total_red': color_totals["Red"],
                'total_green': color_totals["Green"],
                'total_blue': color_totals["Blue"],
                'total': sum(color_totals.values())
            })

            # Return the first detected color with count > 0
            for color, count in color_counts.items():
                if count > 0:
                    cap.release()
                    return color

            time.sleep(0.1)  # Small delay to prevent high CPU usage

    finally:
        cap.release()

def handle_detected_color(color):
    global color_totals
    
    if color in color_totals:
        color_totals[color] += 1
        system_data['color_totals'][color] = color_totals[color]
        system_data['total_sorted'] = sum(color_totals.values())
        
        log_entry = f"{time.strftime('%H:%M:%S')} - Detected {color} color. Total: {color_totals[color]}"
        system_data['logs'].append(log_entry)
        socketio.emit('update_logs', log_entry)
        print(log_entry)
        
        # Update web interface immediately
        socketio.emit('update_counts', {
            'current_red': system_data['color_counts']['Red'],
            'current_green': system_data['color_counts']['Green'],
            'current_blue': system_data['color_counts']['Blue'],
            'total_red': color_totals["Red"],
            'total_green': color_totals["Green"],
            'total_blue': color_totals["Blue"],
            'total': system_data['total_sorted']
        })
        
        if color == "Blue":
            set_servo_angle(servo_1, 150, "Servo 1")
        elif color == "Red":
            set_servo_angle(servo_2, 45, "Servo 2")
        elif color == "Green":
            set_servo_angle(servo_1, 90, "Servo 1")
            set_servo_angle(servo_2, 90, "Servo 2")
    else:
        log_entry = f"{time.strftime('%H:%M:%S')} - No color detected, keeping both servos at 90 degrees."
        system_data['logs'].append(log_entry)
        socketio.emit('update_logs', log_entry)
        print(log_entry)
        set_servo_angle(servo_1, 90, "Servo 1")
        set_servo_angle(servo_2, 90, "Servo 2")

# Start the motors and IR monitoring in separate threads
stepper_thread_1 = threading.Thread(target=run_stepper, args=(MOTOR_PINS_1,), daemon=True)
stepper_thread_2 = threading.Thread(target=run_stepper, args=(MOTOR_PINS_2, True), daemon=True)
ir_sensor_thread = threading.Thread(target=monitor_ir_sensor, daemon=True)

stepper_thread_1.start()
stepper_thread_2.start()
ir_sensor_thread.start()

# Start web interface in a separate thread
from web_interface import start_web_interface
web_interface_thread = threading.Thread(target=start_web_interface, daemon=True)
web_interface_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping system...")
    servo_1.stop()
    servo_2.stop()
    GPIO.cleanup()
