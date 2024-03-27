import smbus2

bus = smbus2.SMBus("/dev/i2c-1")

I2Caddress = 0x07

startByte = 0x0F

pfreq = 2

lspeed = 255
lbrake = 0

rspeed = 0
rbrake = 0

sv0 = 0
sv1 = 0
sv2 = 0
sv3 = 0
sv4 = 0
sv5 = 0

dev = 50

sens = 50

lowbat = 550

i2caddr = 7
i2cfreq = 0

a = bytearray(bytes([startByte, pfreq])+lspeed.to_bytes(2, 'big')+bytes(lbrake)+rspeed.to_bytes(2, 'big')+bytes(rbrake)+bytes(12)+bytes([dev])+sens.to_bytes(2, 'big')+lowbat.to_bytes(2, 'big')+bytes([i2caddr, i2cfreq]))

for b in a:
	bus.write_byte(I2Caddress, b)
