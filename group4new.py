import ev3dev.ev3 as ev3

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
m = ev3.LargeMotor('outA')
n = ev3.LargeMotor('outD')
us = ev3.UltrasonicSensor('in1')

us.mode = 'US-DIST-CM'


# Write your program here.
while True:
    print(us.value(), "mm")
    if (not (us.value() < 100)):
        m.run_timed(speed_sp=-800, time_sp=1000)
        n.run_timed(speed_sp=-800, time_sp=1000)
    else:
        m.run_timed(speed_sp=800, time_sp=1000)
        n.run_timed(speed_sp=800, time_sp=1000)
