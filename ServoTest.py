import RPI.GPIO as GPIO
import time

servo_pin = 18
GPIO_setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_servo_angle(angle):
	duty = angle/18 + 2
	GPIO.output(servo_pin, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(servo_pin, False)
	pwm.ChangeDutyCycle(0)

try:
	set_servo_angle(90)
	set_servo_angle(0)
	set_servo_angle(180)

finally:
	pwm.stop()
	GPIO.cleanup()
