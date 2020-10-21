#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys, os, time, commands
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import datetime

GPIO.setmode(GPIO.BCM)

# Raspberry Pi pin configuration
RST = 24

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()
 
# Clear display.
disp.clear()
disp.display()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.truetype('/usr/share/fonts/truetype/kochi/kochi-gothic-subst.ttf', 16, encoding='unic')

while True:
    # Get time and date
    d = datetime.datetime.today()
    mydate = d.strftime("%m/%d-")
    #'%s/%s-' % (d.month, d.day)
    mytime = d.strftime("%H:%M:%S")
    #'%s:%s:%s' % (d.hour, d.minute, d.second)
    #print mydate + mytime
        
    # Get CPU temp, voltage, clock
    temp = commands.getoutput("vcgencmd measure_temp").split('=')
    volt=commands.getoutput("vcgencmd measure_volts").split('=')
    clock=commands.getoutput("vcgencmd measure_clock arm").split('=')
    ip=commands.getoutput("ifconfig wlan0 | grep 'inetアドレス' | awk '{ print $1 }'").split(':')

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    mystring= mydate + mytime
    draw.text((0,0), mystring, font=font, fill=255)
    mystring= u'CPU温度'
    draw.text((0,40), mystring, font=font, fill=255)

    #draw.text((64,0), volt[1] , font=font, fill=255)
    draw.text((0,20), ip[1] , font=font, fill=255)
    draw.text((64,40), temp[1] , font=font, fill=255)
    disp.image(image)
    disp.display()

    time.sleep(1)
