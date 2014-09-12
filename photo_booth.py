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

#Try to cleanup stray temp images from before
try:
    subprocess.check_output('rm /home/pi/photobooth_images/*.jpg',shell=True)
    subprocess.check_output('rm /home/pi/temp_*.jpg',shell=True)
except:
    pass

while True:
  if (GPIO.input(SWITCH)):
    usbdevs = subprocess.check_output('lsusb', shell=True)#to see if Nikon attached
    snap = 0
    while snap < 4:
      print("pose!")
      GPIO.output(BUTTON_LED, False)
      GPIO.output(POSE_LED, True)
      time.sleep(1.5)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED, True)
        time.sleep(0.4)
      for i in range(5):
        GPIO.output(POSE_LED, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED, True)
        time.sleep(0.1)
      GPIO.output(POSE_LED, False)
      print("SNAP")
      gpout = ""
      if usbdevs.find('Nikon') != -1: #if Nikon found take photo with gphoto
        gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      else: #take photo with raspicam
        timestamp = datetime.now()
        filename = ("/home/pi/photobooth_images/photobooth%02d%02d%02d.jpg" % (timestamp.hour, timestamp.minute, timestamp.second))
        width = 1296 #648 # 2592 # 1296
        height = 972 #968 # 1944 # 972
        quality = 70 # Set jpeg quality (0 to 100)
        settings = ""
        gpout = subprocess.check_output("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), stderr=subprocess.STDOUT, shell=True)

      print(gpout)
      if "ERROR" not in gpout:
        snap += 1
      GPIO.output(POSE_LED, False)
      time.sleep(0.5)
    print("please wait while your photos print...")
    GPIO.output(PRINT_LED, True)
    # build image and send to printer
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    if usbdevs.find('Canon') != -1: #if Canon Selphy found wait longer
        print("Sending to printer...")
        time.sleep(90)
    else:
        print("No printer found... saving photos to archive")
	time.sleep(20)

    print("ready for next round")
    GPIO.output(PRINT_LED, False)
    GPIO.output(BUTTON_LED, True)
