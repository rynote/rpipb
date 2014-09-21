#!/bin/bash

#Check for usb devices
USBDEVS=`lsusb`;

#print to Selphy if Canon is listed as attached USB device
if [[ $USBDEVS == *Canon* ]]
then
    lp -d CP910_Class /home/pi/temp_montage3.jpg
fi

#save copy to archive
suffix=$(date +%H%M%S)
cp /home/pi/temp_montage3.jpg /home/pi/PB_archive/PB_${suffix}.jpg

#save a copy to albert for testing, checking first to see if it is mounted
if [ -d "/mnt/cam/moviez/cam/PB_archive" ]; then
  cp /home/pi/temp_montage3.jpg /mnt/cam/moviez/cam/PB_archive/PB_${suffix}.jpg
fi

#remove temp images
rm /home/pi/photobooth_images/*.jpg
rm /home/pi/temp_*.jpg

