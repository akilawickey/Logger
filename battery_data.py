import csv
import serial

#----------------------------------------------------------------------

def csv_writer(data, path):

    """

    Write data to a CSV file path

    """

    with open(path, "a") as csv_file:

        writer = csv.writer(csv_file)

        

        writer.writerow(data)

#----------------------------------------------------------------------

if __name__ == "__main__":

	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
	ser.flushInput()
	ser.flushOutput()
	count = 0
	

	while True:
	  data_raw = ser.readline()
	  # count = count + 1

	  if "#" in data_raw:

	   print("ok")

	   # if count == 5:
	   print(data_raw.split())
	   csv_writer(data_raw.split(), "vega.csv")
		  # count = 0	
