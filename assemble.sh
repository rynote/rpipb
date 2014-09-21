#!/bin/bash

#Check for usb devices
USBDEVS=`lsusb`;
if [[ $USBDEVS == *Nikon* ]]
then
    mogrify -crop 912x1296+512+0 -resize 580x824 /home/pi/photobooth_images/*.jpg # good  crop for 4 portrait photos taken in landscape  mode
else
    mogrify -crop 684x972+351+0 -resize 580x824 /home/pi/photobooth_images/*.jpg
fi

montage /home/pi/photobooth_images/*.jpg -tile 2x2 -geometry +10+10 /home/pi/temp_montage2.jpg
montage /home/pi/temp_montage2.jpg /home/pi/photobooth_label.jpg -tile 1x2 -geometry +5+5 /home/pi/temp_montage3.jpg

echo "Assembly Complete. Printing..."