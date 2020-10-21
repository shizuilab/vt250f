#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os, time, commands, subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)

GPIO.output(24, GPIO.HIGH)
GPIO.output(25, GPIO.LOW)
time.sleep(5)
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)

os.system('/home/pi/aquestalkpi/AquesTalkPi "システム起動しました" | aplay')

os.system("sudo /home/pi/start-file.sh")

try:
    while True:
        sw_status1 = GPIO.input(26)
        sw_status2 = GPIO.input(23)
        if os.system('pgrep -l youtube-') == 0:
            GPIO.output(24, GPIO.HIGH)
        else:
            GPIO.output(24, GPIO.LOW)

        if os.system('pgrep -l file-') == 0:
            GPIO.output(25, GPIO.LOW)
        else:
            GPIO.output(25, GPIO.HIGH)

        if sw_status1 == 0:
            GPIO.output(24, GPIO.HIGH)
            if os.system('pgrep -l youtube-') == 256:
                print("starting Youtube streameing...")
                os.system("sudo /home/pi/start-youtube.sh")
        elif sw_status2 == 0:
            GPIO.output(25, GPIO.LOW)
            if os.system('pgrep -l file-') == 256:
                print("starting Drive recorder...")
                os.system("sudo /home/pi/start-file.sh")
        else:
            print("no button input...")

        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    GPIO.cleanup()
