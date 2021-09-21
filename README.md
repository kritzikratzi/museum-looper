Museum Looper
=============


This is a looper for multi-screen video installations at museums for raspberry pi. It's not the greatest code, but works reliably. 

Based on 

* A modified version of [omxplayer-sync](https://github.com/turingmachine/omxplayer-sync) (unclear license)
* [OSC.py](https://github.com/ptone/pyosc) (LGPL)


PREPARE
=======

You will need ... 

1. A certain amount of raspberry pi 3 or 4 with raspbian installed
2. An unmanaged switch and network cables to connect them
3. Some kind of wifi/public hotspot during set up
4. One test file for each raspberry (files need to be exactly the same duration)


SETUP ON EACH RASPBERRY
=======================

First grab the files and run the setup: 

1. Make sure your pi is connected to the internet
2. Copy the files in this repository to /home/pi/looper
3. Open a terminal and type

       cd /home/pi/looper
       ./setup.sh

4. Plug in a usb drive with a single mp4 file, or see "update using your laptop" below
5. `reboot`


The setup step is a bit intricate. It will enable the ssh server, set a password and a few other things. 
You will only have to answer basic questions. 

Please read the source code in [setup.sh](setup.sh). It has an explanation what's going on for each step. 


UPDATE VIDEO FILES USING USB
============================

1. Empty the usb drive, format it as ext3,ext4 or extfs
2. Copy a single mp4 file on the drive
3. Plug it into the raspberry you want to

UPDATE VIDEO FILES USING YOUR LAPTOP
====================================

Connect your laptop to the unmanaged switch and set the ip to 192.168.0.240, now you can update your files using

    rsync --progress my_file_1.mp4 pi@192.168.0.114:/home/pi/Videos/main_video.mp4
    rsync --progress my_file_2.mp4 pi@192.168.0.115:/home/pi/Videos/main_video.mp4
    etc.

