import serial
import time
import threading

#from time import time, sleep

from SimpleJoystick import SimpleJoystick

import os

xaxis = 0
yaxis = 0
zaxis = 0

xdelta = 0
ydelta = 0
zdelta = 0


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
    


def listen(ser):
    global xaxis, yaxis, zaxis, xdelta, ydelta, zdelta
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                
                if line[0:6] == "X-axis":
                    xaxis = round(((int(line.split("\t")[-1])+119)/800)*9.8,3)
                    #xaxis = int(line.split("\t")[-1])
                    if (abs(xaxis) <= 0.2):
                        xaxis = 0
                if line[0:6] == "Y-axis":
                    yaxis = round(((int(line.split("\t")[-1])-566)/800)*9.8, 3)
                    #yaxis = int(line.split("\t")[-1])
                    if (abs(yaxis) <= 0.2):
                        yaxis = 0
                if line[0:6] == "Z-axis":
                    zaxis = round(((int(line.split("\t")[-1])-485)/800)*9.8, 3)
                    #zaxis = int(line.split("\t")[-1])
                    if (abs(zaxis) <= 0.4):
                        zaxis = 0
                    
                if line[0:6] == "X-delt":
                    xdelta = int(line.split("\t")[-1])
                if line[0:6] == "Y-delt":
                    ydelta = int(line.split("\t")[-1])
                if line[0:6] == "Z-delt":
                    zdelta = int(line.split("\t")[-1])
                
                if line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] and line[1] != "V":
                    print("Arduino: ", line)
            except:
                pass

class arduino_interface:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

        self.leftSpeed = 0
        self.rightSpeed = 0

        self.brakes = False

        self.servos = [2, 2, 2, 2, 2, 2]

        self.nextSendTime = 0
        
        self.update()
        
        self.turnmode = False
        
        time.sleep(5)

    def startListen(self):
        threading.Thread(target=listen, args=(self.ser,), name="listen", daemon=False).start()
    
    def servoTimer(self):
        time.sleep(2)
        self.servos = [2, 2, 2, 2, 2, 2]
        self.update()
    
    def setTurnMode(self, new):
        if new == self.turnmode:
            return
        
        self.turnmode = new
        
        if new:
            self.servos = [0.5, 0.5, 0.5, 2, 0.5, 2]
        else:
            self.servos = [1, 1, 0, 2, 1, 2]
        
        self.update()
        self.servoTimer()
    
    def update(self):
        
        while time.time_ns() < self.nextSendTime:
            time.sleep(0.1)
            
        self.leftSpeed = max(min(1, self.leftSpeed), -1) # What do these two lines do? -Sam
        self.rightSpeed = max(min(1, self.rightSpeed), -1)
        
        #self.leftSpeed = selectInRange(-1, 1, self.leftSpeed)
        #self.rightSpeed = selectInRange(-1, 1, self.rightSpeed)
        
        leftStr = "{:03d}".format(int(self.leftSpeed*0.75*255+255))
        rightStr = "{:03d}".format(int(self.rightSpeed*0.75*255+255))
        
        #leftStr = f"{int(self.leftSpeed*255+255)}"
        #rightStr = f"{int(self.rightSpeed*255+255)}"
        
        #print(f"Left Speed: {leftStr} Right speed: {rightStr}")

        for i in range(len(self.servos)):
            if self.servos[i] != 2:
                #self.servos[i] = max(min(self.servos[i], 1), 0)
                self.servos[i] = selectInRange(0, 1, self.servos[i])

        if self.brakes:
            #brakeStr = "{:03d}".format(255)
            brakeStr = "255"
        else:
            #brakeStr = "{:03d}".format(0)
            brakeStr = "000"

        servosMsg = ""

        for i in range(len(self.servos)):
            servosMsg += "{:03d}".format(int(self.servos[i]*100))
        
        msg = leftStr+rightStr+brakeStr+servosMsg
        
        print("Sending: ", msg)
        self.ser.write(bytes(msg, 'utf-8'))

        self.nextSendTime = time.time_ns()+100

    def setBrakes(self, brakes):
        self.brakes = brakes
        if brakes:
            self.leftSpeed = 0
            self.rightSpeed = 0
        self.update()
    
    def setServos(self, angles):
        self.servos = angles
        self.update()
        self.servoTimer()
    
    def setServo(self, servo, angle):
        self.servos[servo] = angle
        self.update()
        self.servoTimer()
    
    def setLeftSpeed(self, newSpeed):
        self.leftSpeed = newSpeed
        self.update()

    def setRightSpeed(self, newSpeed):
        self.rightSpeed = newSpeed
        self.update()

    def setMotorSpeed(self, newSpeed):
        self.rightSpeed = newSpeed
        self.leftSpeed = newSpeed
        self.update()
"""
interface = arduino_interface()

interface.setTurnMode(True)

time.sleep(1)

interface.leftSpeed = 1
interface.rightSpeed = -1

interface.update()

time.sleep(1)

interface.setMotorSpeed(0)

time.sleep(1)

interface.setTurnMode(False)
"""

"""

controller = SimpleJoystick()
t1 = time.time()

while True:
    
    output = controller.getValues()
    
    if output["cross"]:
        print("Terminated")
        interface.setMotorSpeed(0)
        break
    elif output["square"]:
        print("60%")
        interface.setMotorSpeed(0.60)
    elif output["triangle"]:
        print("80%")
        interface.setMotorSpeed(0.80)
    elif output["circle"]:
        print("100%")
        interface.setMotorSpeed(1.0)
    else:
        print(f"Custom: {output['y']}")
        interface.setMotorSpeed(output["y"])
    
    print(output)
    
    time.sleep(0.1)
"""

if __name__ == "__main__":
    pass







