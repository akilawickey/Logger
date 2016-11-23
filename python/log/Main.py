
import csv
import serial
import serial.tools.list_ports
import thread
import threading
import time
import Queue
import os
import errno
import time
import struct
import shutil
import sys
import re

from can_h import can
from battery_H import bat
from pyMultiwii import MultiWii
from flight_h import FLIGHTBOARD
from Data_H import data_H
from sys import stdout
from time import sleep
from datetime import datetime
from threading import Thread
#----------------------------------------------------------------------
class Main(object):

	if __name__ == '__main__':

		flight_obj 	= 	FLIGHTBOARD()
		can_obj  	=	can()
		bat_obj		=	bat()
		

		XBEE = "/dev/ttyUSB0"
		BATTERY = "/dev/ttyUSB0"
		CAN = "/dev/ttyUSB0"
		FLIGHT = "/dev/ttyUSB0"
		path_can = "/dev/ttyUSB0"

		try:
			########################## Configure USB ports #################################

			list1 = serial.tools.list_ports.comports()

			# battery_cable = "USB VID:PID=0403:6001 SNR=A50285BI"
			# Xbee1 = "USB VID:PID=0403:6001 SNR=AH03I7PP"
			Flight 	= "USB VID:PID=0403:6001 SNR=AM016X60"
			Xbee 	= "USB VID:PID=0403:6001 SNR=AH03I79P"
			Device 	= "Linux 3.13.0-24-generic ehci_hcd EHCI Host Controller 0000:00:1a.0"
			Device_ = 'Linux 3.13.0-24-generic xhci_hcd xHCI Host Controller 0000:02:00.0'
			VID = 'USB VID:PID=1a86:7523'

			#print(list(serial.tools.list_ports.comports()))s
			for a in range(0,len(list1) ):
			 	if((Device == list1[a][1]) & (VID == list1[a][2]) ):
			  		BATTERY = list1[a][0]
					
			 	if( (Xbee == list1[a][2]) & (Device == list1[a][1]) ):
			  		XBEE = list1[a][0]

			  	if(Flight == list1[a][2]):
			  		FLIGHT = list1[a][0]

			 	if(Device_ == list1[a][1]):
			  		CAN = list1[a][0]

			print "\n----------Com Port Configuration--------------"
			print 'Battery 	:'+BATTERY
			print 'can 		:'+CAN
			print 'xbee 		:'+XBEE
			print 'Flight 		:'+FLIGHT +'\n'
			# ----------Open Xbee Serial Port----------------------			
			ser2 = serial.Serial(XBEE, 115200, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False ) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
			ser2.flushInput()
			ser2.flushOutput()

			# ------------Open Flight Board Serial Port-------------
	    		try:

		    		flight_obj.board = MultiWii(FLIGHT)
		    		t_flight = Thread(target=flight_obj.Accelerometer, args=())
		    		t_flight_G = Thread(target=flight_obj.GPS, args=())
				t_flight.start()
				t_flight_G.start()

				can.path_can 	= CAN

				t_can = Thread(target=can_obj.read_can, args=())
				t_can.start()

				bat.path_can	= BATTERY
				# t_bat = Thread(target=bat_obj.read_battery, args=())
				# t_bat.start()

			except Exception,e: 
				print 'ERROR : '+str(e)

			print 'Pass'
			# ----------------Run and print--------------------
			count=0
		        past_load=''
			while True:
		   		count = count + 1
		   		load = data_H.q.get()
		   		x = len(load)

		   		# print "length : "+str(x)+" Size : "+str(sys.getsizeof(q.get()))+" bytes Pht No : "+str(count)+"\n"+ q.get()
		   		# print data_H.q.get()

		   		send = "####,"+str(x)+","+str(count)+","+load+"!!"
		   		print send
		   		if load != past_load:
		   			ser2.write(send)
		   		past_load = load
				# print str(data_H.q.get())

		except Exception,e: 
				print 'ERROR : '+str(e)