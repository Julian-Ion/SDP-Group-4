
from motors import Motors 
from time import time, sleep 
from PCA9685 import PCA9685


pwm = PCA9685()

pwm.setPWMFreq(50)

for i in range(6):
	
	index = 15-i
	
	print("Turning Servo ", index)
	
	print("Turn 0")
	pwm.setServoPulse(index, 500)

	sleep(0.5)
	
	print("Turn 90")
	
	pwm.setServoPulse(index, 1500)
	
	sleep(0.5)
	
	pwm.setServoPulse(index, 0)
	
	#pwm.setPWM(i, False, False)


mc = Motors() 
speed = 100
run_time = 2

for i in range(6):
	try:
		print("Running motor ", i)
		mc.move_motor(i,speed) 
		start_time = time()
		while time() < start_time + run_time:
		    sleep(0.2) 
		mc.stop_motors()
	except:
		print("Motor ", i, " failed")
		mc.stop_motors()
