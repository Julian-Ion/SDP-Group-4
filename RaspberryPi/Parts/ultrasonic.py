import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

class ultrasonic:
    def __init__(self, channel):
        self.sensor = GroveUltrasonicRanger(channel)

    def stream_distance(self):
        while True:
            distance = self.sensor.get_distance()
            print('{} cm'.format(distance))
    
            if distance < 20:
                print('Distance < 20cm')
                time.sleep(1)
    
            else:
                print('Distance > 20cm')
