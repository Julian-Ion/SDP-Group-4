from motors import Motors 
from time import time, sleep 
# Create an instance of the Motors class used in SDP 
mc = Motors() 
motor_id = 0 # The port that your motor is plugged in to 
speed = 100 # forward = positive, backwards = negative 
run_time = 2 # number of seconds to run motors 

# Move motor with the given ID at your set speed

mc.move_motor(motor_id,speed) 
start_time = time() # Encoder board can be fragile - always use a try/except loop 
while time() < start_time + run_time: 
    #mc.print_encoder_data() 
    sleep(0.2) # Use a sleep of at least 0.1, to avoid errors 
mc.stop_motors()