#!/usr/bin/python

import RPi.GPIO as GPIO
import urllib2
import time
import datetime
import os
import sys
import xml.dom.minidom
from xml.dom.minidom import Node

host = "http://garoahc.appspot.com";
location_opened = "/rest/status/open";
location_closed = "/rest/status/close";
location_macs = "/rest/macs";
token = "/1234";

sensor_pin = 7
pinStatus = True
updateDelay = 300 #5 minutes delay
lastUpdate=0

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

def get_parametro_xml(item, parametroName):
        parametro = item.getElementsByTagName(parametroName)
        parametro = parametro[0]
        for atributo in parametro.childNodes:
                if atributo.nodeType == Node.TEXT_NODE:
                        return atributo.data
def get_macs():
	######Get Data From Router#####
	#macsXml = urllib2.urlopen("http://192.168.1.1/ajaxQueryDevice.gch")
	#macsXml = xml.dom.minidom.parse(macsXml)
	#itensList = macsXml.getElementsByTagName('Parameters')

	#macs_str = ""
	#for iten in itensList:
        #	macs_str = macs_str + get_parametro_xml(iten, "MACAddress") + "_"
	##########

	#####Network Scan#####
	#macs_command = "sudo nmap -sP 192.168.1.1-154 | egrep -o ..:..:..:..:..:.."
        macs_command = "sudo arp-scan --interface eth0 -l | egrep -o ..:..:..:..:..:.."

        cmd = os.popen(macs_command)
        macs_str= cmd.read()
        cmd.close()
	macs_str = macs_str.replace("\n","_")
	##########

        macs_str = macs_str.replace(":","")
        macs_str = macs_str[:-1]

	return macs_str

def update_macs():
	macs_str = get_macs()

	#TODO: Update do post
        macs_url=host+location_macs+"/"+macs_str+token
        print "Updating Macs: "+macs_str
        response = urllib2.urlopen(macs_url)

while True:
	try:
		#Status changed or last change was to long ago.
	        if ( (pinStatus != GPIO.input(sensor_pin)) or ( (time.time()-lastUpdate) >= updateDelay ) ):
        	        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                	print "Updating Status"                
	                update_status()
        	        update_macs()
	        time.sleep(5)
	except:
		print "Unexpected error:", sys.exc_info()[0]
