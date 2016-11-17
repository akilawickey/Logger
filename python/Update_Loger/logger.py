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
#----------------------------------------------------------------------

global ser_can,ser_batt,path_can,q,fifo,lock,CVS_name,board

lock = threading.Lock()
q = Queue.Queue()

dest = '/home/vega/Desktop/logger/Log'
source = '/home/vega/Desktop/logger'

time_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CVS_name = "battery_"+time_+"_.csv"
print CVS_name

def Accelerometer(board):
	while True:
	    try:
	    	global head
	        board.getData(MultiWii.ATTITUDE)
	        angx = board.attitude['angx']
	        angy = board.attitude['angy']
	        head = board.attitude['heading']

	        # print "X : " +str(angx) + " Y : " + str(angy) +" Head : " + str(head)
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

def csv_writer(data, CVS_name):
    with open(CVS_name, "a") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(data)


def read_battery(path_can,Boud):
	ser_batt = serial.Serial(path_can, Boud, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_batt.flushInput()
	ser_batt.flushOutput()

	while True:
		global data_raw
		line = ""
		while True:
			x = ser_batt.readline(1)
			# print str(x)
			line = line + str(x)
			if x == '\n':
				# print line
				break

		if len(line) > 10:
			data_raw = line
			# data_raw = '#0,0,0,0,3,4,5,1,2,4,34,23,43,32,65,23,34,23,43,32  #1,4345,4645,6755,3456,4334,3453,1234,4355,3423,4356,7567,3245,5467,3245,3425,23445,23445,2345,4325,3454,3453,5344,5435,3455,3455,3456,2345,2445,2345,23445,2455,2344,3455,4566,3455,34544,4535,3455,3244,2344,5464,2344,5345,2342,43455,23445,2344,5345,2344,4353'
			# data_raw = ser_batt.readline()
			time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			csv_write_battery = time + str(data_raw)
			csv_writer(csv_write_battery.split(','),CVS_name)
			# print(csv_write_battery)
			# ser2.write("####"+csv_write_battery+"]]]]")
			# fifo.write(csv_write_battery)
			# fifo.close()
			lock.acquire()
			q.put(csv_write_battery)
			lock.release()
			#data_raw = '#0,0,0,0,3,4,5,1,2,4,34,23,43,32,65,23,34,23,43,32  #1,4345,4645,6755,3456,4334,3453,1234,4355,3423,4356,7567,3245,5467,3245,3425,23445,23445,2345,4325,3454,3453,5344,5435,3455,3455,3456,2345,2445,2345,23445,2455,2344,3455,4566,3455,34544,4535,3455,3244,2344,5464,2344,5345,2342,43455,23445,2344,5345,2344,4353'
	    	

def read_can(path_can,Boud):     
	global data_raw2  
	ser_can = serial.Serial(path_can, Boud, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_can.flushInput()
	ser_can.flushOutput()

	while True:
		data_raw2= ser_can.readline()
		# data_raw2 = line
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		csv_write_can = time + str(data_raw2)	

		csv_writer(csv_write_can.split(','), "can.csv")
		# ser2.write("####"+csv_write_can+"]]]]")
		# fifo.write(csv_write_can)
		# fifo.close()
		lock.acquire()
		if q.full():
			q.get()
			print 'Qeue reset'
		q.put(csv_write_can)
		lock.release()
		#data_raw2 = "#ID: BB  Data: 23 45 34 23 45 23 45 23"
	    	# print(csv_write_can)

def findPorts(port,boud):
	ser_batt = serial.Serial(port, boud, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser_batt.flushInput()
	ser_batt.flushOutput()
	data_raw = ser_batt.readline()

	for index in range(len(data_raw)):
   		if(data_raw[index] == "#"):
   			return True

	return False

def progress():
	prg = '#'
	while True:
		prg = prg + ' #'
		print	prg+"\r"
		time.sleep(0.5)	
#----------------------------------------------------------------------

if __name__ == "__main__":
	q = Queue.Queue()
	files = os.listdir(source)
	# fifopath = "/home/vega/Desktop/logger"
	# os.mkfifo(fifopath)
	# fifo = open(fifopath,"w")

	XBEE = ""
	BATTERY = ""
	CAN = ""
	FLIGHT = ""
	DEVICE_1 = '/dev/ttyACM0'
	Device_2 = '/dev/ttyACM0'
	path_can = '/dev/ttyUSB0'

	try:
		########################## Configure USB ports #################################

		list1 = serial.tools.list_ports.comports()

		# battery_cable = "USB VID:PID=0403:6001 SNR=A50285BI"
		# Xbee1 = "USB VID:PID=0403:6001 SNR=AH03I7PP"
		Flight = "USB VID:PID=0403:6001 SNR=AM016X60"
		Xbee =   "USB VID:PID=0403:6001 SNR=AH03I79P"
		Device = "USB VID:PID=1a86:7523"
		flag_p = 0

		#print(list(serial.tools.list_ports.comports()))s
		for a in range(0,len(list1) ):
		 	if(Device == list1[a][2]):
		 		if(flag_p == 0):	
		  			DEVICE_1 = list1[a][0]
		  			flag_p = 1
				
		 	if(Xbee == list1[a][2]):
		  		XBEE = list1[a][0]

		  	if(Flight == list1[a][2]):
		  		FLIGHT = list1[a][0]

		 	if(Device == list1[a][2]):
		  		DEVICE_2 = list1[a][0]

		##################################################################################				
	
		# ser_batt = serial.Serial('/dev/ttyUSB1', 9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		# ser_batt.flushInput()
		# ser_batt.flushOutput()

		# ser_can = serial.Serial('/dev/ttyUSB0', 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		# ser_can.flushInput()
		# ser_can.flushOutput()

		ser2 = serial.Serial(XBEE, 115200, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False ) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser2.flushInput()
		ser2.flushOutput()

		path_ = '/dev/ttyUSB1'
    		# board = MultiWii(path_)
    		board = MultiWii(FLIGHT)
    		t_flight = Thread(target=Accelerometer, args=(board,))
		t_flight.start()

		print "-----------------------------------------------"
		if t_flight.isAlive():
		   		print "Flight started    state : Alive"
		print "-----------------------------------------------"
		#xbee = XBee.XBee("/dev/ttyUSB0") 
		################################################
		IF = 1 # Debuging purposes
		if IF:
			print("VEGA logging data ...")
			print "-----------------------------------------------"
			print "Xbee : " + XBEE
			print "Flight : " + FLIGHT
			print "Device_1 : " + DEVICE_1
			print "Device_2 : " + DEVICE_2
			print "-----------------------------------------------"

			t_device_1 = Thread(target=findPorts, args=(DEVICE_1,115200,))
			t_device_2 = Thread(target=findPorts, args=(DEVICE_2,115200,))

			# t_prg = Thread(target=progress, args=())
			# t_prg.start()

			# t_device_1.start()
			# t_device_2.start()
			
			
			time.sleep(10)

			if(t_device_1.isAlive() & t_device_2.isAlive()):
			 	print "COM port ERROR"

			if(t_device_1.isAlive()):
				CAN = DEVICE_2
				BATTERY = DEVICE_1
				print "CAN : " + DEVICE_2
				print "Battery : " + DEVICE_1
			else:
				CAN = DEVICE_1
				BATTERY = DEVICE_2
				print "CAN : " + DEVICE_1
				print "Battery : " + DEVICE_2




		# if( flag_Device_2 == 1 ):
		# 	print "battery" + DEVICE_2

		# if(state == True):
		# 	print "True"
		# else:
		# 	print "False"
		################################################
		# while True:
		  # thread.start_new_thread(read_battery,())	
		  # read_can()	
		  # read_battery()
		  # read_can()


		try:
		   # thread.start_new_thread( print_time, ("Thread-1", 2, ) )
		   # thread.start_new_thread( print_time, ("Thread-2", 4, ) )
		   #thread.start_new_thread( print_time, ("Amila",) )
		   print "-----------------------------------------------"
		   t_bat = Thread(target=read_battery, args=(BATTERY,9600))
		   t_can = Thread(target=read_can, args=(CAN,115200))
		   t_bat.start()
		   # t_can.start()
		   # t_bat.join()
		   # t_can.join()

		   count=0
		   # if t_bat.isAlive():
		   # 		print "Alive"
		   while True:
		   		count = count + 1
		   		print q.get()
		   		# print str(head)
		   		x = len(q.get())
		   		print x
		   		ser2.write("####"+str(x)+"##"+q.get()+","+str(count)+"$$")
		   		
		   		board.getData(MultiWii.ATTITUDE)
		   		head = board.attitude['heading']
		   		# print str(head)
		   		# print "Main"
		   		time.sleep(1)
		   		if(count % 10 == 0):
		   			# lock.acquire()
		   			# q.queue.clear()
		   			# lock.release()
		   			# print "Cleared"
		   			print str(head)
		   			ser2.write("####"+ str(head) +"$$")

		except KeyboardInterrupt:
				# print files
				for f in files:
					# print str(f)
				# for f in files:
				    if (str(f) == str(CVS_name)):
				        shutil.move(f, dest)
				        print 'Log files saved in folder ' + dest
				print "closing ports"
				t_bat.terminate()
				t_can.terminate()
        			ser_batt.close()
        			ser_can.close()

		except:
		   print "Error: Main loop"

		   # while True:
		   # 		print q.get()
		   # 		ser2.write(q.get())

		  # print("VEGA logging data ...")
		  # time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
		  # if count == 5:
		  # ent = xbee.SendStr(data_raw.split(','))

		  #send_Xbee()
		  #thread.start_new_thread(send_Xbee)
		  

		  # print("sent!!!")
		  # csv_write_battery = time + str(data_raw)	
		  # csv_write_can = time + str(data_raw2)	

		  # csv_writer(csv_write_battery.split(','), "battery.csv")
		  # csv_writer(csv_write_can.split(','), "can.csv")

			  # count = 0	
	except :
		sys.exit(0)
		print "Error: Main"