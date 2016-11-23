#######################################TEAM VEGA##################################################

import csv
import serial
# import XBee
from time import sleep
from datetime import datetime
from threading import Thread #Import by Amila
import serial.tools.list_ports
import thread
import threading
import time
import Queue
import os
import errno
# -------------------------------
from pyMultiwii import MultiWii
from sys import stdout
import time
import struct
import shutil
import sys
import re
# from logger_h import _logger_
#----------------------------------------------------------------------

global ser_can,ser_batt,path_can,q,fifo,lock,lock_x,CVS_name_bat,board,a1,a2,x0,x5

lock = threading.Lock()
lock_x = threading.Lock()
q = Queue.Queue()

# dest = '/home/vega/Desktop/logger/Log'
# source = '/home/vega/Desktop/logger'

time_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

CVS_name_bat_temp =  '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_temp_'+time_+'_.csv'
CVS_name_bat_1_vol = '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_1_vol_'+time_+'_.csv'
CVS_name_bat_2_vol = '/home/vega/Desktop/Logger/python/log/Log/BAT/battery_2_vol_'+time_+'_.csv'
CVS_name_can = 		 '/home/vega/Desktop/Logger/python/log/Log/CAN/can_'+time_+'_.csv'
# print CVS_name_bat

def GPS(board):
    while True:
    	# pass
	    try:
		        # while True:
	        	# lock_x.acquire()
	            board.getData(MultiWii.RAW_GPS)
	            # lock_x.release()
		        # print str(getData.gps)
	            x0 = str(board.gps['I6'])
	            #x
	            x1 = str(board.gps['I2'])
	            x2 = str(board.gps['I3'])
	            # y
	            x3 = str(board.gps['I4'])
	            x4 = str(board.gps['I5'])
	            x5 = str(board.gps['I7'])
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

	            a1 = int(A,2)   # GPS_latitude
	            a2 = int(A1,2)  # GPS_longitude

		            # print "GPS_latitude : " + str(a1)
		            # print "GPS_longitude : " + str(a2)
		            # print "GPS_altitude : " + x0
		            # print "GPS_speed : " + x5

		            # gps_data = "GPS_latitude : " + str(a1) + " , "+"GPS_longitude : " + str(a2)+" , "+"GPS_altitude : " + x0+" , "+ "GPS_speed : " + x5
	            gps_data = 'G,'+str(a1) + "," + str(a2)+","+ str(x0)+","+ str(x5)
	            # print gps_data

	            lock.acquire()
		    if q.full():
			q.get()
			print 'Data droped GPS'
	            else:
			print 'Data added GPS.'
			q.put(gps_data)
		    lock.release()
		            
	            time.sleep(5)


	    except Exception,error:
	    	pass
	        # print "Error on Main: "+str(error)

	    except KeyboardInterrupt:
	        print "EXIT"
	        os._exit(1)

def Accelerometer(board):
	x0=""
	while True:
	    try:
	    	global head,angy,angx
	        board.getData(MultiWii.ATTITUDE)
	        angx = board.attitude['angx']
	        angy = board.attitude['angy']
	        head = board.attitude['heading']


	        # print "X : " +str(angx) + " Y : " + str(angy) +" Head : " + str(head)

	        data = 'D,'+str(angx)+","+str(angy)+","+str(head)

	    	lock.acquire()
		# q.put(data)
		if q.full():
				q.get()
				print 'Data droped XYZ'
		else:
				print 'Data added XYZ.'
		q.put(data)

		lock.release()

	        time.sleep(5)
	    except Exception,error:
	        print "Error on Main: "+str(error)

	    except KeyboardInterrupt:
	        print "EXIT"
	        os._exit(1)
		# return head


def Flight():
	# print "flight start"
	# while True:
		Accelerometer(board)
		# time.sleep(1)

def csv_writer(data, CVS_name_bat):
    with open(CVS_name_bat, "a") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(data)


def read_battery(path_can,Boud):
	ser_batt = serial.Serial(path_can, Boud, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_batt.flushInput()
	ser_batt.flushOutput()

	while True:
		# start_time = time.time()
		global data_raw
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
					csv_write_battery = time1 + str(line)
					csv_writer(csv_write_battery.split(','),CVS_name_bat_temp)

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
				csv_write_battery = time1 + str(line)
				csv_writer(csv_write_battery.split(','),CVS_name_bat_1_vol)
			if no_of_bat == '2':
				csv_write_battery = time1 + str(line)
				csv_writer(csv_write_battery.split(','),CVS_name_bat_2_vol)

			lock.acquire()
			if q.full():
				q.get()
				print 'Data droped : BATTERY'
			q.put(line)
			lock.release()

def read_can(path_can,Boud):     
	global data_raw2  
	ser_can = serial.Serial(path_can, Boud, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_can.flushInput()
	ser_can.flushOutput()

	while True:
		data_raw2= ser_can.readline()

		# for x in xrange(1,len(data_raw2)):
		# 	print data_raw2[0:2]
		send_C = ''
		if (data_raw2[0:6] == 'ID: BB') :
			# print str(data_raw2[23:25])
			trq = data_raw2[26:37].split(' ')
			
			trq_hex = str(trq[1]+trq[2]+trq[3])

			xrF = int(trq_hex, 16)
			xrI = int(trq[0],16)
			# print str(trq[0])

			send_C ='BB,'+str(xrI)+','+str(xrF) 
			# print send_C
		if (data_raw2[0:6] == 'ID: BC') :
			# print str(data_raw2[23:25])
			trq = data_raw2[26:37].split(' ')
			
			trq_hex = str(trq[1]+trq[2]+trq[3])

			xrF = int(trq_hex, 16)
			xrI = int(trq[0],16)
			# print str(trq[0])

			send_C ='BC,'+str(xrI)+','+str(xrF)

		# data_raw2 = 'C,ID: BB  Data: 00 00 00 AA 01 8A 26 59'
		# time.sleep(0.5)

		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		csv_write_can = time + str(data_raw2)	

		csv_writer(csv_write_can.split(','), CVS_name_can)
		# ser2.write("####"+csv_write_can+"]]]]")
		# fifo.write(csv_write_can)
		# fifo.close()
		# print str(data_raw2[0:19])
		lock.acquire()
		if q.full():
			q.get()
			print 'Data droped : CAN'
		send_C = 'C,'+send_C
		q.put(send_C)
		# q.put(t)
		lock.release()
		#data_raw2 = "#ID: BB  Data: 23 45 34 23 45 23 45 23"
	    	# print(csv_write_can)

def findPorts(port,boud):
	ser_batt = serial.Serial(port, boud, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_batt.flushInput()
	ser_batt.flushOutput()

	try:
		data_raw = ser_batt.readline()
		for index in range(len(data_raw)):
	   		if(data_raw[index] == "#"):
	   			return True
		return False
	except:
		print 'Com port Busy'

#----------------------------------------------------------------------

if __name__ == "__main__":
	q = Queue.Queue(maxsize=10)

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
		Flight = "USB VID:PID=0403:6001 SNR=AM016X60"
		Xbee =   "USB VID:PID=0403:6001 SNR=AH03I79P"
		Device = "Linux 3.13.0-24-generic ehci_hcd EHCI Host Controller 0000:00:1a.0"
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
		path_ = '/dev/ttyUSB1'
    		# board = MultiWii(path_)

    		try:

	    		board = MultiWii(FLIGHT)
	    		t_flight = Thread(target=Accelerometer, args=(board,))
	    		t_flight_G = Thread(target=GPS, args=(board,))
			# t_flight.start()
			# t_flight_G.start()
		except Exception,e: 
			print 'ERROR : '+str(e)

		print "-----------------------------------------------"
		if t_flight.isAlive():
		   		print "Flight started    state : Alive"
		print "-----------------------------------------------"

		# ------------Start Main Threads-------------------------
		try:

		   # t_bat = Thread(target=read_battery, args=(BATTERY,9600))
		   t_can = Thread(target=read_can, args=(CAN,115200))
		   # t_bat.start()
		   t_can.start()

		   count=0
		   past_load=''
		   while True:
		   		count = count + 1
		   		load = q.get()
		   		x = len(load)

		   		# print "length : "+str(x)+" Size : "+str(sys.getsizeof(q.get()))+" bytes Pht No : "+str(count)+"\n"+ q.get()
		   		# print q.get()

		   		send = "####,"+str(x)+","+str(count)+","+load+"!!"
		   		print send
		   		if load != past_load:
		   			ser2.write(send)
		   		past_load = load
		   		
		   		# board.getData(MultiWii.ATTITUDE)
		   		# head = board.attitude['heading']

		except KeyboardInterrupt:
				print "closing ports"
				t_bat.terminate()
				t_can.terminate()
        			ser_batt.close()
        			ser_can.close()

		except:
		   print "Error: Main loop"	
	except :
		sys.exit(0)
		print "Error: Main"