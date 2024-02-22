from Controllers.servo_control import Servo_Control
from Controllers.motor_control import Motor_Control
from game_controller import Game_Controller

class Alfred:
    def __init__(self):
        # servo controller
        self.servo_controller = Servo_Control

        # motor controller
        self.motor_controller = Motor_Control

        # game controller
        self.game_controller = Game_Controller
    
    def main(self):
        self.servo_controller.set_angle_all(90)

        while True:
            mode = 1
            button = self.game_controller.controller.get_button(CONTROLLER_BUTTON_A)
            mode = abs(1 + int(button))     # Two modes: 1 is for standard front wheel turning, 2 for all wheel turning

            if mode:
                current_angle = self.game_controller.get_angle()
                self.servo_controller.set_angle_front(current_angle)

                current_speed = self.game_controller.get_speed()
                self.motor_controller.go_all(0.001, current_speed)
            else:
                current_angle = self.game_controller.get_angle()
                self.servo_controller.set_angle_all(current_angle)

                current_speed = self.game_controller.get_speed()
                self.motor_controller.go_all(0.001, current_speed)


alfred = Alfred
alfred.main()