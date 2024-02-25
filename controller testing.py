## IMPORTANT NOTE ##
# this is designed to run from the terminal, running it from idle will still probably work but will be messy

import pygame
import time
import math
import os
import platform

pygame.init()

clock = pygame.time.Clock()

running = True

joysticks = {}

# determines what clear terminal command is needed based on OS may need tweaking
clearCall = 'cls'
if platform.system() == 'Linux':
    clearCall = 'clear'

# controller is a bit duff and can give messy input
deadzone = 0.25

frameCount = 0
# will update the display info every <updateStep> frames
# will still continue to process and provide infor, this is purely visual
updateStep = 15

while running:
    # only update data on screen every couple frames to avoid jittering
    if frameCount == 0:
        os.system(clearCall)
    
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            # if options button pressed program ends
            if event.button == 9:
                running = False

        # handles new device connection, add start up comments in here
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy

        # handles lost connection, may want to add things like turning off motors etc
        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]

    # this structure is from the pygame example code for controller handling
    # built to work with multiple controllers but will be fine for just one too
    joyStick_count = pygame.joystick.get_count()

    for joystick in joysticks.values():

        name = joystick.get_name()
        power_level = joystick.get_power_level()
        
        leftStickLeftRight = joystick.get_axis(0) # (left) -1 -> 1 (right)
        leftStickUpDown = -joystick.get_axis(1) # (up) 1 -> -1 (down)

        rightTrigger = joystick.get_axis(5) # (pressed) 1 -> -1 (unpressed)

        xButton = joystick.get_button(0) # (unpressed) 0 -> 1 (pressed)

        leftStickMag = math.sqrt(leftStickLeftRight*leftStickLeftRight + leftStickUpDown*leftStickUpDown)

        if leftStickMag > deadzone:
            leftStickDirection = (leftStickLeftRight/leftStickMag, leftStickUpDown/leftStickMag)

            # angle is calculated in radians from from y axis (up)
            # measured clockwise from 0 to 2pi
            # ik this is sloppy but whatever
            if leftStickDirection[0] <= 0 and leftStickDirection[1] <= 0: # left down
                leftStickAngle = math.pi-math.asin(leftStickDirection[0])
            if leftStickDirection[0] <= 0 and leftStickDirection[1] > 0: # left up
                leftStickAngle = 2*math.pi+math.asin(leftStickDirection[0])
            if leftStickDirection[0] > 0 and leftStickDirection[1] <= 0: # right down
                leftStickAngle = math.pi-math.asin(leftStickDirection[0])
            if leftStickDirection[0] > 0 and leftStickDirection[1] > 0: # right up
                leftStickAngle = math.asin(leftStickDirection[0])
        else:
            leftStickDirection = (math.nan, math.nan)
            leftStickAngle = math.nan

        if frameCount == 0:
            print(name, power_level)
            print("left right:", leftStickLeftRight)
            print("up down:", leftStickUpDown)
            print("right trigger:", rightTrigger)
            print("x button:", xButton)
            print("Stick mag:", leftStickMag)
            print("stick direction:", leftStickDirection)
            print("stick angle:", leftStickAngle)

        # then do all the logical bits of controlling it

        # what im thinking
            # right trigger is brake
            # left stick forward and backward + car like steering left to right
            # holding x puts it in spot turning mode where the wheels point inwards
                # in spot turning mode it tries to match the stick angle with the 0 angle being
                # whatever direction it was facing when it went into turning mode
            # as well as speed being scaled with the joystick magnitudes

    if len(joysticks) == 0 and frameCount == 0:
        print("no controller detected")
    
    frameCount += 1
    frameCount = frameCount%updateStep
    clock.tick(30)


## SHUT DOWN PROCEEDURE ##
# put all necesary shut down commands (like turning off motors etc) here before pygame.quit()



pygame.quit()
        

        
