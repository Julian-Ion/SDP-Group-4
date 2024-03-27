from smbus import SMBus





def main() -> None:
    ic2bus = SMBus(1)
    ic2_address = 0x07
    
    ic2bus.write_byte(ic2_address, 0xEF)


if __name__ == "__main__":
    main()




# 1 Start byte – must be 0x0F (15 decimal)
# 2 PWM frequency – a number from 1 to 7 to select motor PWM frequency
# 3 Left motor speed high byte
# 4 Left motor speed low byte
# 5 Left motor brake – 0=brake off
# 6 Right motor speed high byte
# 7 Right motor speed low byte
# 8 Right motor brake – 0=brake off
# 9 Servo 0 position high byte
# 10 FServo 0 position low byte
# 11 Servo 1 position high byte
# 12 Servo 1 position low byte
# 13 Servo 2 position high byte
# 14 Servo 2 position low byte
# 15 Servo 3 position high byte
# 16 Servo 3 position low byte
# 17 Servo 4 position high byte
# 18 Servo 4 position low byte
# 19 Servo 5 position high byte
# 20 Servo 5 position low byte
# 21 Accelerometer de-vibrate 0-255
# 22 Impact sensitivity high byte
# 23 impact sensitivity low byte
# 24 lowbat high byte
# 25 lowbat low byte
# 26 I2C address 0-127
# 27 clock frequency – 0=100kHz

