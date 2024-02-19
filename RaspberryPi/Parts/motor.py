from motors import Motors
from time import time, sleep

class Motor:
    def __init__(self, channel):
        self.id = channel
        self.speed = 100
        self.mc = Motors()

    def go(self, run_time):
        self.mc.move_motor(self.id, self.speed)
        sleep(run_time)
        self.mc.stop_motors()

    def reverse(self, run_time):
        self.mc.move_motor(self.id, - self.speed)
        sleep(run_time)
        self.mc.stop_motors()
    
    def set_speed(self, new_speed):
        # new_speed is between 1 and 100
        new_speed = max(min(new_speed, 100), 1)
        self.speed = new_speed
