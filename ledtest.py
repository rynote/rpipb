#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess

from datetime import datetime #for raspistill filename

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

while True:
    print("print led ON")
    GPIO.output(PRINT_LED, True)
    time.sleep(0.5)
    GPIO.output(PRINT_LED, False)
    print("print led OFF")
    time.sleep(0.5)


