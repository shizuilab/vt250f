#!/bin/bash
ID='046d:0825'
MATCHES=$(lsusb | sed -n 's/Bus \([0-9]*\) Device \([0-9]*\): ID '$ID'.*/\/dev\/bus\/usb\/\1\/\2/p')
if [ -z ${MATCHES} ]; then
 echo "No match found"
else
 sudo /home/pi/usbreset $MATCHES
fi
