from Parts.motor import Motor

class Motor_Control:
    # define motors, allows for public access to servo
    motor_front_left = Motor(0)
    motor_front_right = Motor(1)
    motor_middle_left = Motor(2)
    motor_middle_right = Motor(3)
    motor_rear_left = Motor(4)
    motor_rear_right = Motor(5)     # Exact motor number may change later

    def go_all(self, run_time):
        self.motor_front_left.set_angle(run_time)
        self.motor_front_right.set_angle(run_time)
        self.motor_middle_left.set_angle(run_time)
        self.motor_middle_right.set_angle(run_time)
        self.motor_rear_left.set_angle(run_time)
        self.motor_rear_right.set_angle(run_time)
