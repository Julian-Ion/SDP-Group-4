import RPi.GPIO as IO
import time
from numpy import interp

IO.setwarnings(False)
IO.setmode(IO.BCM)

class Servo:
    MIN_DEGREE = 0
    MAX_DEGREE = 180
    INIT_DUTY = 2.5

    def __init__(self, channel):
        IO.setup(channel,IO.OUT)
        self.pwm = IO.PWM(channel,50)
        self.pwm.start(self.INIT_DUTY)

    def __del__(self):
        self.pwm.stop()

    def set_angle(self, angle):
        # Map angle from range 0 ~ 180 to range 25 ~ 125
        angle = max(min(angle, self.MAX_DEGREE), self.MIN_DEGREE)
        tmp = interp(angle, [0, 180], [25, 125])
        wait_time = round((tmp / 10) * 0.2, 2)
        self.pwm.ChangeDutyCycle(round(tmp/10.0, 1))
        time.sleep(wait_time)
