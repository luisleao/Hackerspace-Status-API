#!/usr/bin/python

import RPi.GPIO as GPIO
import urllib2
import time
import datetime
import os
import sys

host = "http://garoahc.appspot.com";
location_opened = "/rest/status/open";
location_closed = "/rest/status/close";
location_macs = "/rest/macs";
token = "/1234";

sensor_pin = 7
pinStatus = True
updateDelay = 300 #5 minutes delay
lastUpdate=0
macs = []

#SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def update_status():
    global pinStatus
    global lastUpdate

    readStatus = GPIO.input(sensor_pin)

    status_url=host
    if(readStatus):
        #Open
        print "Opened"
        status_url+=location_opened
    else:
        #Closed
        print "Closed"
        status_url+=location_closed

    status_url+=token
    response = urllib2.urlopen(status_url)

    pinStatus = readStatus
    lastUpdate = time.time()

def get_macs():
    #####Network Scan#####
    #macs_command = "sudo nmap -sP 192.168.1.1-154 | egrep -o ..:..:..:..:..:.."
    macs_command = "sudo arp-scan --interface eth0 -l | egrep -o ..:..:..:..:..:.."

    cmd = os.popen(macs_command)
    macs_str= cmd.read()
    cmd.close()
    
    macs_str = macs_str[:-1]
    ##########

    return macs_str.split('\n')

def update_macs(macsl):
    macs_str = "_".join(macsl)
    macs_str = macs_str.replace(":","")
    
    #TODO: Update to post
    macs_url=host+location_macs+"/"+macs_str+token
    print "Updating Macs: "+macs_str
    response = urllib2.urlopen(macs_url)

while True:
    try:
        macs=macs + get_macs()
        macs = list(set(macs))
        print "Number of Macs: " + len(macs)
        
        #Status changed or last change was to long ago.
        if ( (pinStatus != GPIO.input(sensor_pin)) or ( (time.time()-lastUpdate) >= updateDelay ) ):
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            print "Updating Status"
            update_status()
            update_macs(macs)
            macs=[]
        time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception,e:
        print str(e)