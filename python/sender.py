import csv
import serial
# import XBee
from time import sleep
from datetime import datetime
import serial.tools.list_ports

#----------------------------------------------------------------------




def csv_writer(data, path):

    """

    Write data to a CSV file path

    """

    with open(path, "a") as csv_file:

        writer = csv.writer(csv_file,delimiter=',')

        

        writer.writerow(data)

#----------------------------------------------------------------------

if __name__ == "__main__":


	XBEE = ""
	BATTERY = ""
	CAN = ""


	try:

		########################## Configure USB ports #################################

		list1 = serial.tools.list_ports.comports()
		Xbee = "USB VID:PID=0403:6001 SNR=AH03I7PP"
		battery_cable = "USB VID:PID=0403:6001 SNR=A50285BI"
		CAN_pid_vid = "USB VID:PID=1a86:7523"


		#print(list(serial.tools.list_ports.comports()))
		for a in range(0,len(list1) ):
		    #if(list1[a][0] ==  "/dev/ttyUSB0"):
		 if(list1[a][2] == CAN_pid_vid):	
		  CAN = list1[a][0]
				
		 if(Xbee == list1[a][2]):
		  XBEE = list1[a][0]

		 if(battery_cable == list1[a][2]):
		  BATTERY = list1[a][0]

		##################################################################################				
		print CAN
		ser = serial.Serial(CAN, 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser.flushInput()
		ser.flushOutput()
		count = 0

		ser2 = serial.Serial(XBEE, 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser2.flushInput()
		ser2.flushOutput()

		
		#xbee = XBee.XBee("/dev/ttyUSB0") 
		

		while True:
		  data_raw = ser.readline()
		  # count = count + 1

		  
		  print("ok")
		  time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
		  # if count == 5:
		  print(data_raw)
		  # ent = xbee.SendStr(data_raw.split(','))
		  ser2.write('###' +time + '#' + str(data_raw)+ ']]]]]]]')
		  print("sent")
		  csv_write = time + str(data_raw)	
		  csv_writer(csv_write.split(','), "CAN.csv")
			  # count = 0	
	except KeyboardInterrupt:

		print "closing ports"
        ser.close()
        
