#!/bin/sh

sudo pkill -SIGTERM -f youtube-
sudo pkill -SIGTERM -f file-

sleep 10

sudo systemctl stop youtube
sudo systemctl stop filetube

/home/pi/aquestalkpi/AquesTalkPi "VT250F システムを終了します　お疲れさまでした" | aplay

exit 0

