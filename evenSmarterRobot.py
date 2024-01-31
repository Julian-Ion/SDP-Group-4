import ev3dev.ev3 as ev3
import curses
import time

# This program allows controlling an EV3 robot with arrow keys.
# It requires the 'curses' library to capture key presses.

# Create your objects here.
m_a = ev3.LargeMotor('outA')
m_b = ev3.LargeMotor('outD')

us = ev3.UltrasonicSensor('in1')
us.mode = 'US-DIST-CM'  # Set the mode of the UltrasonicSensor to measure distance in cm.

def robot_control(window):
    # Set up the window parameters
    window.nodelay(True)  # Don't wait for user input
    key = ""  # Placeholder for the key press

    # Instructions for the user
    window.addstr("Control the robot with arrow keys. 'q' to exit.\n")

    while key != ord('q'):  # Run until 'q' is pressed
        key = window.getch()  # Get the key press

        distance = us.value() / 10  # Convert to cm
        # window.addstr("Distance: {} cm".format(distance))

        if key == curses.KEY_UP:  # If the up arrow key is pressed
            m_a.run_forever(speed_sp=500)
            m_b.run_forever(speed_sp=500)
        elif key == curses.KEY_DOWN:  # If the down arrow key is pressed
            m_a.run_forever(speed_sp=-500)
            m_b.run_forever(speed_sp=-500)
        elif key == curses.KEY_LEFT:  # If the left arrow key is pressed
            m_a.run_forever(speed_sp=-500)
            m_b.run_forever(speed_sp=500)
        elif key == curses.KEY_RIGHT:  # If the right arrow key is pressed
            m_a.run_forever(speed_sp=500)
            m_b.run_forever(speed_sp=-500)
        else:
            m_a.stop(stop_action="coast")
            m_b.stop(stop_action="coast")

        if distance < 20:  # If the robot is too close to an object
            # window.addstr(" Object detected! ")
            m_a.stop(stop_action="brake")
            m_b.stop(stop_action="brake")

        window.refresh()

# Set up curses wrapper to handle the window creation
curses.wrapper(robot_control) 