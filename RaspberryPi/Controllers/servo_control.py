from Parts.servo import Servo

class Servo_Control:
    # define servos, allows for public access to servo
    servo_front_left = Servo(12) # PWM
    servo_front_right = Servo(16)
    servo_middle_left = Servo(18)
    servo_middle_right = Servo(22)
    servo_rear_left = Servo(24)
    servo_rear_right = Servo(26)

    def set_angle_front(self, angle):
        self.servo_front_left.set_angle(angle)
        self.servo_front_right.set_angle(angle)
    
    def set_angle_all(self, angle):
        self.servo_front_left.set_angle(angle)
        self.servo_front_right.set_angle(angle)
        self.servo_middle_left.set_angle(angle)
        self.servo_middle_right.set_angle(angle)
        self.servo_rear_left.set_angle(angle)
        self.servo_rear_right.set_angle(angle)
