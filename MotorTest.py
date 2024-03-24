
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
motor_pin_forward = 2
motor_pin_backward = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin_forward, GPIO.OUT)
GPIO.setup(motor_pin_backward, GPIO.OUT)

def motor_forward(seconds):
	GPIO.output(motor_pin_forward, GPIO.HIGH)
	GPIO.output(motor_pin_backward, GPIO.LOW)
	time.sleep(seconds)
	GPIO.output(motor_pin_forward, GPIO.LOW)

def motor_backward(seconds):
	GPIO.output(motor_pin_backward, GPIO.HIGH)
	GPIO.output(motor_pin_forward, GPIO.LOW)
	time.sleep(seconds)
	GPIO.output(motor_pin_backward, GPIO.LOW)

try:
	motor_forward(5)
	time.sleep(2)
	motor_backward(5)

finally:
	GPIO.cleanup()
