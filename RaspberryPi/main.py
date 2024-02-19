from Controllers.servo_control import Servo_Control
from Controllers.motor_control import Motor_Control

class Alfred:
    def __init__(self):
        # servo controller
        self.servo_controller = Servo_Control

        # motor controller
        self.motor_controller = Motor_Control
    
    def main(self):
        self.servo_controller.set_angle_all(90)

alfred = Alfred
alfred.main()