#!/bin/sh


sudo pkill -SIGTERM -f youtube-
sudo pkill -SIGTERM -f file-

sleep 8

sudo systemctl stop youtube
sudo systemctl stop filetube

sleep 8

/home/pi/aquestalkpi/AquesTalkPi "VT250F システムを終了します　お疲れ様でした" | aplay

exit 0

