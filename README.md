rpipb
=====

Photobooth with a Raspberry Pi

Modified from http://www.instructables.com/id/Raspberry-Pi-photo-booth-controller/?ALLSTEPS

sudo wget raw.github.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh

Basically:
Install gphoto
sudo chmod 755 gphoto2-updater.sh
sudo ./gphoto2-updater.sh

To ensure your camera mounts properly to be controlled via USB remove these files:

sudo rm /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
sudo rm /usr/share/gvfs/mounts/gphoto2.mount
sudo rm /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor
sudo rm /usr/lib/gvfs/gvfs-gphoto2-volume-monitor

Restart:
sudo shutdown -r 0

Install CUPS for printing:
sudo apt-get install cups
sudo usermod -a -G lpadmin pi

http://127.0.0.1:631
This will open up the CUPS setup.
Click "administration" and "add printer;" enter your username and password (e.g., the defaults "pi" and "raspberry").

You should see your printer listed under "local printer;" select it and click "continue."
Set the name and location of your printer as you like, and click "continue."
Select the driver for your printer. For me, there was no CP900 driver, but the CP770 driver worked just fine.
Set the default options.

**Add a Class if you want to use a pool of printers... then print to the pool!

Check for active printers
lpstat -p

Install ImageMagik
sudo apt-get install imagemagick


mkdir -p ~/scripts/photobooth
cd ~/scripts/photobooth

Get these scripts, make them executable.
sudo chmod 755 *

Edit the "assemble_and_print" script. Change the "lp" line to include your printer name (or Class).
sudo nano assemble_and_print

Make directories for assembling the montage and archiving shots.
mkdir ~/photobooth_images
mkdir ~/PB_archive

Copy a label for photos to ~/:
scp photobooth_label.jpg pi@rpicam.local:~

Set script to run automatically.

sudo nano /etc/rc.local
insert: /home/pi/scripts/photobooth/startup_script &
above the "exit 0" line

Restart the RPi
sudo shutdown -r 0

