#!/usr/bin/python

from gps import *
from time import *
import os, time, commands, datetime
import urllib
import pprint
import json
import sys
import threading

gpsd = None

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

# Main program loop:
if __name__ == '__main__':
    firstFixFlag = False
    firstFixDate = ""
    gpsp = GpsPoller()
    try:
        gpsp.start()
        while True:
            print(gpsd.fix.mode)
            if gpsd.fix.mode==3:
                # If the sentence shows that there's a fix, then we can log the line
                if firstFixFlag is False:
                    # If we haven't found a fix before, set the filename prefix with GPS date & time.
                    firstFixDate = gpsd.utc
                    firstFixFlag = True
                else: # write the data to a simple log file and then the raw data as well:
                    #print gpsd.utc, gpsd.fix.longitude, gpsd.fix.latitude
                    filename = "/media/pi/USB0/gpslog/" + firstFixDate + "-simple-log.txt"
                    with open(filename.replace(':','') , "a") as myfile:
                        simple_log_line = gpsd.utc + "," + str(gpsd.fix.latitude) + "," + str(gpsd.fix.longitude)
                        simple_log_line = simple_log_line.replace('T',',')
                        print (simple_log_line)
                        myfile.write(simple_log_line + "\n")
                    with open("/var/tmp/lnglat.txt", "w") as myfile:
                        lnglat = str(gpsd.fix.longitude) + "," + str(gpsd.fix.latitude)
                        print (lnglat)
                        myfile.write(lnglat)

            else: # in case gpsData is not available just put nodata into /var/tmp/lnglat.txt
                with open("/var/tmp/lnglat.txt", "r") as myfile:
                    lnglat = myfile.read()
                with open("/var/tmp/lnglat.txt", "w") as myfile:
                    myfile.write(lnglat)
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing
    print "Done.\nExiting."
