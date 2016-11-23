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

class bat(object):

	def read_battery(self):

		self.path_can
		d_obj = data_H()
		data_H.CVS_name_bat	= data_H.CVS_name_bat_1_vol  

		ser_batt = serial.Serial(self.path_can, 9600, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_batt.flushInput()
		ser_batt.flushOutput()

		while True:
			# start_time = time.time()
			line = ""
			no_of_bat = ''
			time.sleep(0.001)
			
			x = ser_batt.readline(1)
			
			# if x == '#':
			# 	while True:	
			# 		x = ser_batt.readline(1)
			# 		if (x == '$'):
			# 			line = ""
			# 		# else:
			# 		# if (x != '#') | (x != '$'):
			# 		line = line + str(x)
			# 		if (x == '\n') | (x == '\t'):
			# 			print str(line)
			# 			lenb = len(line)
			# 			if lenb < 75:
			# 				line = 'T,' + line
			# 			else:
			# 				line = 'B,' + line
			# 			break
			#---------------------------------------
			if x == '#':
				while True:	
					x = ser_batt.readline(1)

					time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
					

					if (x == '$'):
						line = ""
					line = line + str(x)
					if x == '\t':
						# print str(line)
						line = 'T,' + line
						data_H.CVS_name_bat	= data_H.CVS_name_bat_temp  
						csv_write_battery = time1 + str(line)
						data_H.data = csv_write_battery
						data_H.csv_writer(d_obj)

						break
					if x =='\n':
						if line[0] =='$':
							# print str(line[3])
							no_of_bat = str(line[3])
						else:
							# print str(line[1])
							no_of_bat = str(line[1])
									
						line = 'B,' + line
						break
			#---------------------------------------
				# print no_of_bat
				if no_of_bat == '1':
					data_H.CVS_name_bat	= data_H.CVS_name_bat_1_vol
					csv_write_battery = time1 + str(line)
					data_H.data = csv_write_battery
					data_H.csv_writer(d_obj)
				if no_of_bat == '2':
					data_H.CVS_name_bat	= data_H.CVS_name_bat_2_vol
					csv_write_battery = time1 + str(line)
					data_H.data = csv_write_battery
					data_H.csv_writer(d_obj)

				data_H.lock.acquire()
				if data_H.q.full():
					data_H.q.get()
					print 'Data droped : BATTERY'
				data_H.q.put(line)
				data_H.lock.release()

