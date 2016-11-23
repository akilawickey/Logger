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

from sys import stdout
from time import sleep
from datetime import datetime
from threading import Thread

class data_H(object):
	time_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	CVS_name_bat_temp =  '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_temp_'+time_+'_.csv'
	CVS_name_bat_1_vol = '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_1_vol_'+time_+'_.csv'
	CVS_name_bat_2_vol = '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_2_vol_'+time_+'_.csv'
	CVS_name_can = 		 '/home/vega/Desktop/Logger/python/log/Log/CAN/can_'+time_+'_.csv'

	lock = threading.Lock()
	q = Queue.Queue(maxsize=10)

	def csv_writer(self):
	    self.CVS_name_bat
	    with open(self.CVS_name_bat, "a") as csv_file:
	    	self.data
	        writer = csv.writer(csv_file,delimiter=',')
	        writer.writerow(self.data)
		