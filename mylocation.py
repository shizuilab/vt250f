#!/usr/bin/python
# -*- coding: utf-8 -*-
# 配信用に時刻、住所、気温、湿度、気圧を整形

import os, time, commands, datetime
import urllib
import pprint
import json
import sys

d = datetime.datetime.today()
mylocation = d.strftime("%Y年%m月%d日%H時%M分")

# Temp, Hum and Pressure

with open("/var/tmp/temperature.txt", "r") as myfile:
    mytemperature = myfile.read()
with open("/var/tmp/humidity.txt", "r") as myfile:
    myhumidity = myfile.read()
with open("/var/tmp/pressure.txt", "r") as myfile:
    mypressure = myfile.read()

mylocation = mylocation + " 気温" + mytemperature + "℃ 湿度" + myhumidity + "％ 気圧" + mypressure + "hPa" 

# Weather
APP_ID = "dj0zaiZpPUhFckxmNlZqMDRubSZzPWNvbnN1bWVyc2VjcmV0Jng9ZDM-"

# BASE_URL = "http://weather.olp.yahooapis.jp/v1/place"
COORDINATES = ""

with open("/var/tmp/lnglat.txt", "r") as myfile:
    COORDINATES = myfile.read()
if COORDINATES == "":
    with open("/var/tmp/locationbuff.txt", "w") as myfile:
        myfile.write(mylocation)
    os.system('sudo mv /var/tmp/locationbuff.txt /var/tmp/location.txt')
    sys.exit()
else:
    print(COORDINATES)

OUTPUT="json"

# Reverse Geocoding from Coodinates
ZIP_BASE_URL = "https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder"
zip_url = ZIP_BASE_URL + "?appid=%s&coordinates=%s&output=%s" % (APP_ID,COORDINATES,OUTPUT)
zip_json_tree = json.loads(urllib.urlopen(zip_url).read())
name = zip_json_tree['Feature'][0]['Property']['Address']
if len(name) > 0:
    #mylocation = mylocation + "\n" + "仮想通貨取引実況中  "
    mylocation = mylocation + "\n" + name.encode('utf_8') + " "
else:
    with open("/var/tmp/locationbuff.txt", "w") as myfile:
        myfile.write(mylocation)
    os.system('sudo mv /var/tmp/locationbuff.txt /var/tmp/location.txt')
    sys.exit()

# Weather forcast from Coordinates
BASE_URL = "https://map.yahooapis.jp/weather/V1/place"
url = BASE_URL + "?appid=%s&coordinates=%s&output=%s" % (APP_ID,COORDINATES,OUTPUT)
json_tree = json.loads(urllib.urlopen(url).read())
#print(json_tree)

for var in range(0,1):
    date     = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Date']
    rainfall = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Rainfall']
    type     = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Type']
    rain_level = ""
    talk = ""
    if (rainfall == 0.0):
        rain_level = "雨は降"
    elif (rainfall < 5.0) :
        rain_level = "雨が少し降"
    elif (rainfall < 10.0):
        rain_level = "雨が降"
    elif (rainfall < 20.0):
        rain_level = "強めの雨が降"
    elif (rainfall < 30.0):
        rain_level = "雨が強く降"
    elif (rainfall < 50.0):
        rain_level = "雨が激しく降"
    elif (rainfall < 80.0):
        rain_level = "非常に激しい雨が降"
    elif (rainfall >= 80.0):
        rain_level = "猛烈な雨が降"

    if type == "observation" :
        time = " 今"
        if rainfall == 0.0:
            suffix = "っていません"
            talk = time + rain_level + suffix
        else:
            suffix = "っています"
            talk = time + rain_level + suffix
    else:
        time = "\n" + str(var * 10) + "分後、"
        if rainfall == 0.0:
            # suffix = "りません。"
            talk = ""
        else:
            suffix = "るかもしれません"
            talk = time + rain_level + suffix

    #print talk
    if len(talk) > 0:
        mylocation = mylocation + talk

with open("/var/tmp/locationbuff.txt", "w") as myfile:
    myfile.write(mylocation)
os.system('sudo mv /var/tmp/locationbuff.txt /var/tmp/location.txt')
print(mylocation)
