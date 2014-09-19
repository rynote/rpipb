#!/usr/bin/python

import time, os, subprocess

from datetime import datetime #for raspistill filename

import sys, pygame

#os.environ["SDL_FBDEV"] = "/dev/fb1"
# Init framebuffer/touchscreen environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

pygame.init()
size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
img_ready = pygame.image.load("pb_screens/ready.jpg")
img_working = pygame.image.load("pb_screens/working.jpg")
img_printing = pygame.image.load("pb_screens/printing.jpg")
img_star = pygame.image.load("pb_screens/star.jpg")
img_1 = pygame.image.load("pb_screens/1.jpg")
img_2 = pygame.image.load("pb_screens/2.jpg")
img_3 = pygame.image.load("pb_screens/3.jpg")


def cleanupTempFiles():
    try:
        subprocess.check_output('rm /home/pi/photobooth_images/*.jpg',shell=True)
        subprocess.check_output('rm /home/pi/temp_*.jpg',shell=True)
    except:
        pass

def showCountdown():
    showBlack()
    time.sleep(.5)
    
    print("pose!")
    screen.blit(img_3,(0,0))
    pygame.display.flip()  
    time.sleep(1)
	
    screen.blit(img_2,(0,0))
    pygame.display.flip()
    time.sleep(1)
    
    screen.blit(img_1,(0,0))
    pygame.display.flip()
    time.sleep(1)
    
    print("SNAP")
    screen.blit(img_star,(0,0))
    pygame.display.flip()

def showWorking():
    print("working...")
    screen.blit(img_working,(0,0))
    pygame.display.flip()

def showPrinting():
    print("printing...")
    screen.blit(img_printing,(0,0))
    pygame.display.flip()

def showBlack():
    print("black...")
    screen.fill(black)
    pygame.display.flip()
	
def showReady():
    print("ready to take photos")	
    screen.blit(img_ready,(0,0))
    pygame.display.flip()
    pygame.event.clear()

def takePhotos():
    global busy
    busy = True
    usbdevs = subprocess.check_output('lsusb', shell=True)#to see if Nikon attached
    snap = 0
    while snap < 4:
        showCountdown()

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
            
    # build image and send to printer
    showWorking()   
    subprocess.call("sudo /home/pi/scripts/photobooth/assemble_and_print", shell=True)
    
    if usbdevs.find('Canon') != -1: #if Canon Selphy found wait longer
        showPrinting()
        print("Sending to printer...")
        time.sleep(90)
    else:
        print("No printer found... saving photos to archive")
        time.sleep(20)
	
    showReady()
    busy = False


cleanupTempFiles()
showReady()
busy = False

while 1:
    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONUP:
        x , y = event.pos
        print ("screen touched at: (%d , %d)" % event.pos)
        if (x > 240) & (y > 160):
            sys.exit(1)
        pygame.mouse.set_pos([0,0])
        busy = True
        takePhotos()

