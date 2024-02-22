import pygame
from numpy import interp

class Game_Controller:
    controller = pygame.controller(0)

    def get_angle(self):
        left_x = self.controller.get_axis(CONTROLLER_AXIS_LEFTY)
        tmp_x = interp(left_x, [-32768, 32767], [0, 180])
        return tmp_x

    def get_speed(self):
        left_y = self.controller.get_axis(CONTROLLER_AXIS_LEFTX)
        tmp_y = interp(left_y, [-32768, 32767], [-50, 50])
        return tmp_y