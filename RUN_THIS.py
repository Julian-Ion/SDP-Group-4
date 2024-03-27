#from controller-testing import controller
from SimpleJoystick import SimpleJoystick
from arduino_interface import ArduinoInterface
from time import sleep
import platform
import os


class Controller:
	
    def __init__(self) -> None:
        
        self.CONTROLLER_TEST: bool = True
            
        self.JOYSTICK: SimpleJoystick = SimpleJoystick()
        if not self.CONTROLLER_TEST: self.ARDUINO_INTERFACE: ArduinoInterface = ArduinoInterface()
        else: self.ARDUINO_INTERFACE = None
        self.SYSTEM: str = platform.system()

        return None
    
    def transformRange(self, val: float) -> float:
        """
        Transform value in range 0.1-1 to range 0.6-1
        0.6-1 is the range that the motors actually start doing something
        """
        if val < 0:
            val = -val
            returner = (val - 0.1) * (1 - 0.6) / (1 - 0.1) + 0.6
            return -returner
        else:
            return (val - 0.1) * (1 - 0.6) / (1 - 0.1) + 0.6
    
    def clear(self) -> None:

        if self.SYSTEM in ["Linux", "Darwin"]:
            os.system("clear")
        else:
            os.system("cls")

        return None

    def main(self) -> None:

        output = self.JOYSTICK.getValues()
        while not output["cross"]:

            turning: bool = bool(output["square"])
            if not self.CONTROLLER_TEST:
                self.ARDUINO_INTERFACE.setTurnMode(turning)

            if turning: # Turning
                x_speed: float = self.transformRange(output["x"])
                print(f"Square: Turning {x_speed}")
                if not self.CONTROLLER_TEST:
                    self.ARDUINO_INTERFACE.leftSpeed = x_speed
                    self.ARDUINO_INTERFACE.rightSpeed = -x_speed
                    self.ARDUINO_INTERFACE.update()
            elif output["triangle"]:
                print("Triangle: Set speed 0.7")
                if not self.CONTROLLER_TEST:
                    self.ARDUINO_INTERFACE.setMotorSpeed(0.7)
            elif output["circle"]:
                print("Circle: Set speed 1")
                if not self.CONTROLLER_TEST:
                    self.ARDUINO_INTERFACE.setMotorSpeed(1.0)
            else:
                y_speed: float = self.transformRange(output["y"])
                print(f"No buttons: Manual Speed {y_speed}")
                if y_speed <= -0.6 or y_speed >= 0.6:
                    if not self.CONTROLLER_TEST:
                        self.ARDUINO_INTERFACE.setMotorSpeed(y_speed)
                else:
                    if not self.CONTROLLER_TEST:
                        self.ARDUINO_INTERFACE.setMotorSpeed(0.0)

            sleep(0.1)
            self.clear()
            output = self.JOYSTICK.getValues()

        return None


def main() -> None:
    controller = Controller()
    controller.main()
    return None


if __name__ == "__main__":
    main()
