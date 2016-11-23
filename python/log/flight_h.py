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

from pyMultiwii import MultiWii
from sys import stdout
from time import sleep
from datetime import datetime
from threading import Thread
from Data_H import data_H
#-----------------------------------------------------------------------------------------------
class FLIGHTBOARD(object) :

	# q = Queue.Queue(maxsize=10)

	def GPS(self):
		self.board
	    	while True:
	    	# pass
		    try:
			        # while True:
		        	# lock_x.acquire()
		            self.board.getData(MultiWii.RAW_GPS)
		            # lock_x.release()
			        # print str(getData.gps)
		            x0 = str(self.board.gps['I6'])
		            #x
		            x1 = str(self.board.gps['I2'])
		            x2 = str(self.board.gps['I3'])
		            # y
		            x3 = str(self.board.gps['I4'])
		            x4 = str(self.board.gps['I5'])
		            x5 = str(self.board.gps['I7'])
		            # print x3
		            # print x4

		            x = x1[2:len(x1)]
		            y = x2[2:len(x2)]

		            x1 = x3[3:len(x3)]
		            y1 = x4[2:len(x4)]

		            if(len(x) != 16):
		                for n in xrange(0,16 - len(x)):
		                    x = '0' + x

		            if(len(y) != 16):
		                for n in xrange(0,16 - len(y)):
		                    y = '0' + y

		            if(len(x1) != 16):
		                for n in xrange(0,16 - len(x1)):
		                    x1 = '0' + x1

		            if(len(y1) != 16):
		                for n in xrange(0,16 - len(y1)):
		                    y1 = '0' + y1

		            A = y + x
		            A1= y1 + x1

		            # print 'GPS'

		            a1 = int(A,2)   # GPS_latitude
		            a2 = int(A1,2)  # GPS_longitude

			            # print "GPS_latitude : " + str(a1)
			            # print "GPS_longitude : " + str(a2)
			            # print "GPS_altitude : " + x0
			            # print "GPS_speed : " + x5

			            # gps_data = "GPS_latitude : " + str(a1) + " , "+"GPS_longitude : " + str(a2)+" , "+"GPS_altitude : " + x0+" , "+ "GPS_speed : " + x5
		            gps_data = 'G,'+str(a1) + "," + str(a2)+","+ str(x0)+","+ str(x5)
		            # print gps_data
		            
		            data_H.lock.acquire()
			    if data_H.q.full():
				data_H.q.get()
				print 'Data droped XYZ'
			    else:
			 	print 'Data added XYZ.'
			    data_H.q.put(gps_data)
			    data_H.lock.release()

		            time.sleep(2)


		    except Exception,error:
		    	pass
		        # print "Error on Main: "+str(error)

		    except KeyboardInterrupt:
		        print "EXIT"
		        os._exit(1)

	def Accelerometer(self):
		x0=""
		while True:
		    try:
		    	global head,angy,angx
		        self.board.getData(MultiWii.ATTITUDE)
		        angx = self.board.attitude['angx']
		        angy = self.board.attitude['angy']
		        head = self.board.attitude['heading']


		        # print "X : " +str(angx) + " Y : " + str(angy) +" Head : " + str(head)

		        data = 'D,'+str(angx)+","+str(angy)+","+str(head)
		        data_H.lock.acquire()
		        if data_H.q.full():
				data_H.q.get()
				print 'Data droped XYZ'
			else:
			 	print 'Data added XYZ.'
		        data_H.q.put(data)
		        data_H.lock.release()

		 #    	lock.acquire()
			# # q.put(data)
			# if q.full():
			# 		q.get()
			# 		print 'Data droped XYZ'
			# else:
			# 		print 'Data added XYZ.'
			# q.put(data)

			# lock.release()

		        time.sleep(2)
		    except Exception,error:
		        print "Error on Main: "+str(error)

		    except KeyboardInterrupt:
		        print "EXIT"
		        os._exit(1)
			# return head