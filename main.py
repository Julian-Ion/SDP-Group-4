import ev3dev.ev3 as ev3

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
m = ev3.LargeMotor("outA")
n = ev3.LargeMotor("outD")


# Write your program here.
while True:
    m.run_timed(speed_sp=200, time_sp=1000)
    n.run_timed(speed_sp=200, time_sp=1000)
