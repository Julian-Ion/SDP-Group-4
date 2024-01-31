import ev3dev.ev3 as ev3

# Docstring explaining the purpose and usage of the program
"""
This program allows a LEGO EV3 robot to be controlled via command line input.
It takes directional commands (forward, back, left, right) and uses an
ultrasonic sensor to avoid obstacles within 100 units of distance.
"""
try:
    # Create your objects here.
    m = ev3.LargeMotor('outA')
    n = ev3.LargeMotor('outD')
    us = ev3.UltrasonicSensor('in2')

    # Set the mode of the ultrasonic sensor
    us.mode = 'US-DIST-CM'

    def get_direction():
        """
        Prompts the user to input a direction command and returns the command.

        Returns:
            string: The command input by the user ('forward', 'back', 'left', 'right').
        """
        return input("Enter direction (forward, back, left, right): ").lower()

    def move_robot(direction):
        """
        Moves the robot based on the direction command provided by the user.

        Args:
            direction (string): The direction in which to move the robot.
        """
        # Define the speed for the motors
        speed = 800
    
        # Check for obstacles using the ultrasonic sensor
        distance = us.value()
        if distance < 100:Program terminated by user.

        # Control logic for moving the robot
        if direction == 'forward':
            m.run_forever(speed_sp=speed)
            n.run_forever(speed_sp=speed)
        elif direction == 'back':
            m.run_forever(speed_sp=-speed)
            n.run_forever(speed_sp=-speed)
        elif direction == 'left':
            m.run_forever(speed_sp=-speed)
            n.run_forever(speed_sp=speed)
        elif direction == 'right':
            m.run_forever(speed_sp=speed)
            n.run_forever(speed_sp=-speed)
        else:
            print("Invalid direction!")

    # Main loop
    try:
        while True:
            direction = get_direction()
            move_robot(direction)
    except KeyboardInterrupt:
        # Stop the motors before exiting
        m.stop()
        n.stop()
        print("Program terminated by user.")

except:
    m.stop()
    n.stop()
    print("Program Crashed")