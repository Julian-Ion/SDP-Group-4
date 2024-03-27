import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
s = [0]

time.sleep(1) # Give it a moment to establish connection

ser.reset_input_buffer()

print("Sending stop")
ser.write(b"0")
line = ser.readline().decode('utf-8').rstrip()
print(line)
line = ser.readline().decode('utf-8').rstrip()
print(line)

time.sleep(1)

print("Sending bytes")
ser.write(b"200")
line = ser.readline().decode('utf-8').rstrip()
print(line)
line = ser.readline().decode('utf-8').rstrip()
print(line)

time.sleep(5)

print("Sending stop")
ser.write(b"0")
line = ser.readline().decode('utf-8').rstrip()
print(line)
line = ser.readline().decode('utf-8').rstrip()
print(line)

