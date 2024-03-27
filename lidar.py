import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
import math

import requests

port = "/dev/ttyUSB0";
baud_rate = 230400;

print("\n>port:", port," baud_rate:", baud_rate );


try:
	lidarSerial = serial.Serial( port, baud_rate )
	print(">lidar connect:", lidarSerial.isOpen())

except serial.serialutil.SerialException:
	print("\n>lidar connect error...")
	exit()

def draw():
        global is_plot
        while is_plot:
                plt.figure(1)
                plt.cla()
                plt.ylim(-5000, 5000)
                plt.xlim(-5000, 5000)
                plt.scatter(x, y, c='r', s=8)
                plt.pause(0.001)
        plt.close("all")

def send():
    global dataComplete
    while True:
        params={'data':str(data)}
        req = requests.get("https://sam-mccormack.co.uk/SDP2/endpoints/endpoint_lidar.php", params=params)
        req.close()
        print("data sent")
        dataComplete = False
        time.sleep(0.1)

data = []
dataComplete = False

is_plot = True
x = []
y = []
for _ in range(360):
        x.append(0)
        y.append(0)
        data.append(0)

def poll():

	start_count = 0
	got_scan = False
	shutting_down_ = False
	raw_bytes = np.zeros( 2520 , dtype='bytes' )

	good_sets = 0
	motor_speed = 0
	rpms = 0
	index = 0

	while True:
		readByte = None
		try:
			#Wait until first data sync of frame: 0xFA, 0xA0
			readByte = lidarSerial.read(1)	

			if(start_count == 0):
				if( readByte == b'\xfa'):
					start_count = 1
					byte0 = readByte
			else:
				if(start_count == 1):
					byte1 = readByte
					if( readByte == b'\xa0' ):
						start_count = 0

						# Now that entire start sequence has been found, read in the rest of the message
						got_scan = True

						b_result = bytearray()
						received = lidarSerial.read(2518)

						b_result.extend( byte0 ); b_result.extend( byte1 ); b_result.extend( received )

						raw_bytes = bytes(b_result)
						#print(">raw_bytes len:",len(raw_bytes) )

						# scan->angle_min = 0.0;
						# scan->angle_max = 2.0*M_PI;
						# scan->angle_increment = (2.0*M_PI/360.0);

						## Detection distance --> 120mm ~ 3,500mm
						# scan->range_min = 0.12;
						# scan->range_max = 3.5;

						# scan->ranges.resize(360);
						# scan->intensities.resize(360);

						#read data in sets of 6
						for i in range(0, len(raw_bytes), 42):

							if(raw_bytes[i] == 250 and raw_bytes[i+1] == ( 160 + i / 42)): #&& CRC check

								good_sets+=1;
								motor_speed += (raw_bytes[i+3] << 8) + raw_bytes[i+2]; # accumulate count for avg. time increment
								rpms=(raw_bytes[i+3]<<8|raw_bytes[i+2])/10;

								for j in range(i+4, i+40, 6):

									index = 6*(i/42) + (j-4-i)/6

									# Four bytes per reading
									byte0 = raw_bytes[j]; 	byte1 = raw_bytes[j+1]
									byte2 = raw_bytes[j+2]; byte3 = raw_bytes[j+3]

									# Remaining bits are the range in mm
									intensity = (byte1 << 8) + byte0;

									# Last two bytes represent the uncertanty or intensity, might also be pixel area of target...
									# uint16_t intensity = (byte3 << 8) + byte2;
									ranges = (byte3 << 8) + byte2;
									
									if ranges == 0:
										ranges = 4200

									# scan->ranges[359-index] = range / 1000.0;
									# scan->intensities[359-index] = intensity;

									#print(">r[",359-index,"]=", ranges / 1000.0 );
									x[int(359-index)] = (ranges)*math.cos(math.radians(index))
									y[int(359-index)] = (ranges)*math.sin(math.radians(index))
									data[int(359-index)] = ranges
					# scan->time_increment = motor_speed/good_sets/1e8;

					else:
						start_count = 0
		except Exception as e:
			print("\n>lidar pool() exception was thrown: ", e)
			time.sleep(2)

#threading.Thread(target=draw).start()
#threading.Thread(target=send).start()

#poll()

threading.Thread(target=poll).start()
draw()

exit()
