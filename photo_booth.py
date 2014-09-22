#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess

from datetime import datetime #for raspistill filename

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
#RESET = 25
#GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)


#initialize the global variables
usbdevs = 0
busy = False


###################
# Display functions
###################

def showCountdown()
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

def showWorking()
    GPIO.output(POSE_LED, False)

def showPrinting()
    print("please wait while your photos print...")
    GPIO.output(POSE_LED, False)
    GPIO.output(PRINT_LED, True)

def showReady()
    GPIO.output(PRINT_LED, False)
    GPIO.output(POSE_LED, False)
    GPIO.output(BUTTON_LED, True)

###################
# Utility functions
###################

def checkCamera():
    global usbdevs
    usbdevs = subprocess.check_output('lsusb', shell=True)#to see if Nikon attached
    if usbdevs.find('Nikon') != -1:
        return True
    else:
        return False

def cleanupTempFiles():
    try:
        subprocess.check_output('rm /home/pi/photobooth_images/*.jpg',shell=True)
        subprocess.check_output('rm /home/pi/temp_*.jpg',shell=True)
    except:
        pass

def snapPhoto()
    pass

def doAssemble()
    # build image
    print("photos are being processed...")
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble.sh", shell=True)


def doPrint()
    print("please wait while your photos print...")
    subprocess.call("sudo /home/pi/scripts/photobooth/print.sh", shell=True)
    pass

def initCallback()
    GPIO.add_event_detect(SWITCH,GPIO.FALLING, callback=cb_takePhotos, bouncetime=1000)

def disableCallback()
    GPIO.remove_event_detect(SWITCH)

###################
# The Callback function (the mEAT)
###################

def cb_takePhotos(input_pin):
    global busy
    if busy == False:
        disableCallback() #disable the button
        busy = True
        useDSLR = checkCamera()
        usePrinter = (usbdevs.find('Canon') != -1)
        snap = 0
        while snap < 4:
            showCountdown()
            gpout = ""
            if useDLSR #if Nikon found take photo with gphoto
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

        showWorking()
        #doAssemble()
        subprocess.call("sudo /home/pi/scripts/photobooth/print.sh", shell=True)

        showPrinting()
        #doPrinting()
        subprocess.call("sudo /home/pi/scripts/photobooth/print.sh", shell=True)

        if usePrinter: #if Canon Selphy found wait longer
            print("Sending to printer...")
            time.sleep(35)
        else:
            print("No printer found... saving photos to archive")
	        time.sleep(20)

    cleanupTempFiles()
    showReady()
    busy = False
    initCallback() #enable the button again

############
# start here
############

initCallback()
cleanupTempFiles()
showReady()


#i think we need a loop in here somewhere
while not Busy:
    time.sleep(.1)
