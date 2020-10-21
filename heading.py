#!/usr/bin/python3

import time, math
from lsm303d import LSM303D
import pandas as pd

lnglat = [136.780208,35.458272] # default current position is home
destination = lnglat # default destination is home

#destination = [136.733861,35.466949] # default destination is university

lsm = LSM303D(0x1d)  # Change to 0x1e if you have soldered the address jumper

last_heading = 0.0

a = 6378137.0
b = 6356752.314140 #hunipe's constants 

xmax = 0.3302
ymax = 0.2404
zmax = 0.3104

xmin = -0.2244
ymin = -0.2197
zmin = -0.2445

xcalib = (xmax + xmin)/2
ycalib = (ymax + ymin)/2
zcalib = (zmax + zmin)/2

xscale = xmax - xmin
yscale = ymax - ymin
zscale = zmax - zmin

while True:
    try:
        lnglat_input = pd.read_csv("/var/tmp/lnglat.txt", header=None)
        lnglat = lnglat_input.values.tolist()[0]
        destination_input = pd.read_csv("/var/tmp/destination.txt", header=None)
        destination = destination_input.values.tolist()[0]
    except:
        print('error in loading location data')

    if destination[0] < 0.1:
        direct = 0.0
        dist = 0.0
        with open("/var/tmp/heading.txt", "w") as myfile:
            myfile.write(str(round(direct,1)))
        with open("/var/tmp/distance.txt", "w") as myfile:
            myfile.write(str(round(dist,1)))
        continue

    axyz = lsm.accelerometer()
    raw_mxyz = lsm.magnetometer()

    mx = raw_mxyz[0]
    my = raw_mxyz[1]
    mz = raw_mxyz[2]

    mx = mx - xcalib
    my = my - ycalib
    mz = mz - zcalib

    mx = (mx - xmin)/xscale * 2 -1
    my = (my - ymin)/yscale * 2 -1
    mz = (mz - zmin)/zscale * 2 -1

    accXnorm = axyz[0]/math.sqrt(axyz[0]*axyz[0] + axyz[1]*axyz[1] + axyz[2]*axyz[2])
    accYnorm = axyz[1]/math.sqrt(axyz[0]*axyz[0] + axyz[1]*axyz[1] + axyz[2]*axyz[2])

    pitch = math.asin(accXnorm);
    roll = -math.asin(accYnorm/math.cos(pitch))

    magXcomp = mx*math.cos(math.asin(accXnorm))+mz*math.sin(pitch)
    magYcomp = -(mx*math.sin(math.asin(accYnorm/math.cos(pitch)))*math.sin(math.asin(accXnorm))\
                +my*math.cos(math.asin(accYnorm/math.cos(pitch)))-mz*math.sin(math.asin(accYnorm/math.cos(pitch)))*math.cos(math.asin(accXnorm)))

    heading = 180*math.atan2(magYcomp,magXcomp)/math.pi

    if heading < 0:
        heading = heading + 360

    #heading = last_heading + 0.1 * (heading - last_heading)

    homelngrad = destination[0] / 180 * math.pi
    homelatrad = destination[1] / 180 * math.pi
    currentlngrad = lnglat[0] / 180 * math.pi
    currentlatrad = lnglat[1] / 180 * math.pi

    dy = currentlatrad - homelatrad
    dx = currentlngrad - homelngrad
    my = (currentlatrad + homelatrad) / 2
    
    e2 = (a * a - b * b) / (a * a)
    Mnum = a * (1 - e2)
    W = math.sqrt(1 - e2 * math.sin(my) * math.sin(my))
    M = Mnum / W * W * W
    N = a / W

    dist = math.sqrt((dy * M) * (dy * M) + (dx * N * math.cos(my)) * (dx * N * math.cos(my))) / 1000 #自宅距離km

    Y = math.cos(homelatrad) * math.sin(homelngrad - currentlngrad)
    X = math.cos(currentlatrad) * math.sin(homelatrad) \
        - math.sin(currentlatrad) * math.cos(homelatrad) * math.cos(homelngrad - currentlngrad)
    direct = math.atan2(Y, X) * 180 / math.pi #目的地の方角 360度

    if direct < 0:
        direct = direct + 360

    direct = direct - heading #+ 7.333

    if direct > 180:
        direct = direct - 360

    if direct < -180:
        direct = direct + 360

    #last_heading = heading

    print(("heading:{:6.2f} direct:{:6.2f} dist:{:6.2f} pitch:{:6.2f} roll:{:6.2f}").format(heading, direct, dist, pitch, roll))

    with open("/var/tmp/heading.txt", "w") as myfile:
        myfile.write(str(round(direct,1)))
    with open("/var/tmp/distance.txt", "w") as myfile:
        myfile.write(str(round(dist,1)))

    time.sleep(0.5)

