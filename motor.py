#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

motordirect = 0.0 #set 0 at start
clockwise = True
 
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
coil_A_1_pin = 17 # pink
coil_A_2_pin = 18 # orange
coil_B_1_pin = 27 # blue
coil_B_2_pin = 22 # yellow
 
# adjust if different
StepCount = 8
Seq = [[1,0,0,1],
 [1,0,0,0],
 [1,1,0,0],
 [0,1,0,0],
 [0,1,1,0],
 [0,0,1,0],
 [0,0,1,1],
 [0,0,0,1]]
 
#GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
#GPIO.output(enable_pin, 1)
 
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
 
if __name__ == '__main__':
    delay = 2
    steps = 1

    while True:
        with open("/var/tmp/heading.txt", "r") as myfile:
            try:
                heading = float(myfile.read())
                difference = motordirect - heading
                print(heading, difference)

                if difference > 180:
                    difference = difference - 360
                if difference < -180:
                    difference = difference + 360

                if difference > 0 :
                    steps = difference * 512 / 360
                    forward(int(delay) / 1000.0, int(steps))
                elif difference < 0 :
                    steps = -difference * 512 / 360
                    backwards(int(delay) / 1000.0, int(steps))
                motordirect = heading
            except:
                print('float error')
                
            time.sleep(1)
