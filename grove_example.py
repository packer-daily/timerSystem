from machine import I2C, Pin
from grove_lcd import GroveLCD  # If saved as grove_lcd.py

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = GroveLCD(i2c)

lcd.write_line("Hello World!", row=0)
lcd.write_line("RP2040 + Grove", row=1)
