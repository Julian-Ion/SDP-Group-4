"""
Name: interface_ev3
Author: Eliot
Group: group 4
Date: 31.01.24
Description:
Basic interface to abstract basic movement controls of the ev3. Ideally, we should change this code with code to drive
whatever final device is used to control the system (e.g. raspberry pi) but the fundamentals should remain similar
to easily change the system. 
"""

# Import relevant packages.
import ev3dev.ev3 as ev3

# Create objects, will need changed as ports change.
motor_left = ev3.LargeMotor('outA')
motor_right = ev3.LargeMotor('outD')
us_front = ev3.UltrasonicSensor('in4')
us_back = ev3.UltrasonicSensor('in3')

us_front.mode = 'US-DIST-CM'
us_back.mode = 'US-DIST-CM'

# Defined speed, how fast the bot will drive.
abs_speed = 800 # roughly 0.3 m/s

# Standard move forward, backward a set distance. 
# Takes an int distance and calculates relevant values to traverse that distance.
def move(distance):
    time = (distance / 0.3) * (10 ** 3)
    motor_left.run_timed(speed_sp=-abs_speed, time_sp=time) # Motors are attatched backwards, so negative speed is used
    motor_right.run_timed(speed_sp=-abs_speed, time_sp=time)

# Standard turning function. It will turn on the spot but due to limitations, it might not actually turn the distance expect.
# Takes an int angle and turns that many degrees.
def turn(angle):
    pass
