import serial
import threading
from time import sleep
import os


def selectInRange(low:int, high:int, value: int) -> int:
    """
    Returns:
        low if value < low
        high if value > high
        value otherwise
    """
    if value >= high:
        return high
    else:
        return max(low, value)


class ArduinoInterface:

    def __init__(self) -> None:
        
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

        # MOTORS

        self.left_speed: float = 0.0
        self.right_speed: float = 0.0

        # SERVOS

        self.NUM_SERVOS: int = 6
        self.servos: list[float] = [2.0 for _ in range(self.NUM_SERVOS)]

        # TURNING

        self.turning: bool = False

        # OTHER

        self.brakes: bool = False
        self.DEBUG: bool = True

        # MAIN LOOP

        self.finished: bool = False
        self.TIMEOUT: float = 50/1000
        threading.Thread(target=self.update, daemon=True).start()

        # THREADING

        self.lock = threading.Lock()
        self.updated: bool = True

    def debugPrint(self, msg: str) -> None:
        if self.DEBUG:
            self.clear()
            print(msg)

        return None
    
    def clear(self) -> None:

        if self.SYSTEM in ["Linux", "Darwin"]:
            os.system("clear")
        else:
            os.system("cls")

        return None

    # Main loop

    def update(self) -> None:
        """
        Send updates to arduino every x seconds until end signal received
        """
        while not self.finished:

            if self.updated:
                self.updated = False

                # Motors
                
                self.left_speed = selectInRange(-1, 1, self.left_speed)
                self.right_speed = selectInRange(-1, 1, self.right_speed)

                # Turn into a string after calculation and pad with 0s on the left, e.g. 5 => 005
                left_motors_string: str = "{:03d}".format(int((self.left_speed*255)+255))
                right_motors_string: str = "{:03d}".format(int(self.right_speed*255+255))

                # Brakes

                if self.brakes:
                    brakes_string: str = "255"
                else:
                    brakes_string: str = "000"

                # Servos

                servos_string: str = ""
                for i in range(self.NUM_SERVOS):
                    if self.servos[i] != 2.0:
                        self.servos[i] = selectInRange(0, 1, self.servos[i])
                    servos_string += "{:03d}".format(int(self.servos[i]*100))

                # Compile message
                    
                message: str = f"{left_motors_string}{right_motors_string}{brakes_string}{servos_string}"

                self.debugPrint(f"Sending: {message}")

                self.ser.write(bytes(message, 'utf-8'))

                sleep(self.TIMEOUT)

        return None

    def quit(self) -> None:
        """
        End the main update loop and close the program.
        """
        self.finished = True
        return None
    
    # Turning

    def resetServos(self) -> None:
        sleep(2)
        self.setServos(2.0)
        return None

    def setTurnMode(self, mode: bool) -> None:

        if mode == self.turning:
            return None
        
        self.turning = mode

        with self.lock:

            if self.turning:
                self.servos = [0.5, 0.5, 0.5, 2.0, 0.5, 2.0]
            else:
                self.servos = [1.0, 1.0, 0.0, 2.0, 1.0, 2.0]

        self.updated = True
        self.resetServos()

        return None

    # Getters and Setters

    def setLeftSpeed(self, speed: float) -> None:
        """
        Set speed for all left motors
        """
        if not isinstance(speed, float):
            print(f"Speed should be float not {type(speed)}")
            return None
        
        with self.lock:
            self.left_speed = speed

        self.updated = True
        return None

    def getLeftSpeed(self) -> float:
        """
        Get speed for all left motors
        """
        return self.left_speed
    
    def setRightSpeed(self, speed: float) -> None:
        """
        Set speed for all right motors
        """
        if not isinstance(speed, float):
            print(f"Speed should be float not {type(speed)}")
            return None

        with self.lock:
            self.right_speed = speed

        self.updated = True
        return None

    def getRightSpeed(self) -> float:
        """
        Get speed for all right motors
        """
        return self.right_speed
    
    def setDualSpeed(self, speed: float) -> None:
        """
        Set motor speed for both sides
        """
        if not isinstance(speed, float):
            print(f"Speed should be float not {type(speed)}")
            return None
        
        with self.lock:
            self.left_speed = speed
            self.right_speed = speed

        self.updated = True
        return None
    
    def setServos(self, angle: float) -> None:
        """
        Set angle for all servos
        """
        if not isinstance(angle, float):
            print(f"Angle should be float not {type(angle)}")
            return None

        with self.lock:
            self.servos = [angle for _ in range(self.NUM_SERVOS)]

        self.updated = True
        return None
    
    def getServos(self) -> list[float]:
        """
        Get angles for all servos
        """
        return self.servos

    def setServo(self, angle: float, servo_index: int) -> None:
        """
        Set angle for specific servo
        """
        if not isinstance(angle, float):
            print(f"Angle should be float not {type(angle)}")
            return None
        
        if not isinstance(servo_index, int):
            print(f"Servo index should be int not {type(servo_index)}")
            return None

        if 0 <= servo_index and servo_index < self.NUM_SERVOS:
            with self.lock:
                self.servos[servo_index] = angle
        else:
            print(f"Attempted to set servo {servo_index} in range 0-{self.NUM_SERVOS}")

        self.updated = True
        return None
    
    def getServo(self, servo_index: int) -> float:
        """
        Get angle for specific servo
        """
        if not isinstance(servo_index, int):
            print(f"Servo index should be int not {type(servo_index)}")
            return None

        if 0 <= servo_index and servo_index < self.NUM_SERVOS:
            with self.lock:
                return self.servos[servo_index]
        else:
            print(f"Attempted to get servo {servo_index} in range 0-{self.NUM_SERVOS}")
        
        return None
    
    def setBrakes(self, brakes: bool) -> None:
        """
        Turn on or off the brakes
        """
        if not isinstance(brakes, bool):
            print(f"Brakes should be bool not {type(brakes)}")
            return None
        
        self.brakes = brakes
        if self.brakes:
            self.setDualSpeed(0.0)

        self.updated = True
        return None
        

def main() -> None:
    return None


if __name__ == "__main__":
    main()
