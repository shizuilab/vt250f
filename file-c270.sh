#!/bin/bash

set -e

sudo /home/pi/usbreset.sh

sleep 5

if [ ! -e /dev/video0 ]; then
 /home/pi/aquestalkpi/AquesTalkPi "ビデオカメラが見つかりません" | aplay
exit 0
fi

if [ ! -d /media/pi/3DF7-5138/webcam ]; then
 #if [ ! -d /media/pi/USB01/webcam ]; then
 /home/pi/aquestalkpi/AquesTalkPi "USBメモリがみつかりません" | aplay
 exit 0
fi

if [ -f /var/tmp/location.txt ]; then

 /home/pi/aquestalkpi/AquesTalkPi "ドライブレコーダーは停止しています" | aplay

 #ffmpeg -f v4l2 -thread_queue_size 8192\
 #-input_format yuyv422 -video_size 640x360 -framerate 30 -i /dev/video0\
 #-vf drawtext="fontfile=/usr/share/fonts/truetype/fonts-japanese-gothic.ttf:\
 #fontcolor=#FFFFFF:fontsize=20:x=10:y=10:box=1:boxcolor=black@0.4:\
 #textfile='/var/tmp/location.txt':reload=1"\
 #-c:v h264_omx  -b:v 1500k -bufsize 1500k -vsync 0 -t 600\
 #/media/pi/3DF7-5138/webcam/`date +%Y%m%d_%H%M%S`.mp4
 #/media/pi/USB01/webcam/`date +%Y%m%d_%H%M%S`.mp4

else

 /home/pi/aquestalkpi/AquesTalkPi "ロケーションファイルを作製します" | aplay
 date > /var/tmp/location.txt

 #ffmpeg -f v4l2 -thread_queue_size 8192\
 #-f alsa -thread_queue_size 8192 -i plughw:1,0\
 #-input_format yuyv422 -video_size 640x360 -framerate 30 -i /dev/video0\
 #-vf drawtext="fontfile=/usr/share/fonts/truetype/fonts-japanese-gothic.ttf:\
 #fontcolor=#FFFFFF:fontsize=20:x=10:y=10:box=1:boxcolor=black@0.4:\
 #text='%{localtime}'"\
 #-c:v h264_omx  -b:v 1500k -bufsize 1500k -vsync 0  -t 600\
 #/media/pi/3DF7-5138/webcam/`date +%Y%m%d_%H%M%S`.mp4
 #/media/pi/USB01/webcam/`date +%Y%m%d_%H%M%S`.mp4

fi
