import os
import subprocess
import sys

required_packages = [
    "RPi.GPIO",
    "numpy",
    "opencv-python",
    "opencv-python-headless",
    "flask",
    "flask-socketio",
    "eventlet"  # Needed for flask-socketio real-time support
]

def install_packages():
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[✓] Installed: {package}")
        except subprocess.CalledProcessError:
            print(f"[✗] Failed to install: {package}")

if __name__ == "__main__":
    print("Installing required libraries...")
    install_packages()
    print("Done!")
