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

from Data_H import data_H
from sys import stdout
from time import sleep
from datetime import datetime
from threading import Thread

class can(object):

	def read_can(self):

		self.path_can

		d_obj = data_H()

		data_H.CVS_name_bat	= data_H.CVS_name_can  

		data_raw2		= ''  
		ser_can 		= serial.Serial(self.path_can,115200, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_can.flushInput()
		ser_can.flushOutput()

		while True:
			data_raw2= ser_can.readline()

			# for x in xrange(1,len(data_raw2)):
			# 	print data_raw2[0:2]
			self.send_C = ''
			if (data_raw2[0:6] == 'ID: BB') :
				# print str(data_raw2[23:25])
				trq = data_raw2[26:37].split(' ')
				
				trq_hex = str(trq[1]+trq[2]+trq[3])

				xrF = int(trq_hex, 16)
				xrI = int(trq[0],16)
				# print str(trq[0])

				self. send_C ='BB,'+str(xrI)+','+str(xrF) 
				# print send_C
			if (data_raw2[0:6] == 'ID: BC') :
				# print str(data_raw2[23:25])
				trq = data_raw2[26:37].split(' ')
				
				trq_hex = str(trq[1]+trq[2]+trq[3])

				xrF = int(trq_hex, 16)
				xrI = int(trq[0],16)
				# print str(trq[0])

				self.send_C ='BC,'+str(xrI)+','+str(xrF)

			# data_raw2 = 'C,ID: BB  Data: 00 00 00 AA 01 8A 26 59'
			# time.sleep(0.5)

			time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			csv_write_can = time+' ' + str(data_raw2)	

			data_H.data = csv_write_can.split(',')

			# data_H.csv_writer(csv_write_can.split(','), data_H.CVS_name_can)

			data_H.csv_writer(d_obj)

			data_H.lock.acquire()
			if data_H.q.full():
				data_H.q.get()
				print 'Data droped : CAN'
			self.send_C = 'C,'+ self.send_C
			data_H.q.put(self.send_C)
			data_H.lock.release()