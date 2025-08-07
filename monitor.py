from machine import I2C, Pin
from grove_lcd import GroveLCD
import time

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = GroveLCD(i2c)

lcd.write("Hello World!")
lcd.set_cursor(0,1)
lcd.write("RP2040 + Grove")
time.sleep_ms(1000)
lcd.clear()
lcd.scroll_text("This is a long sentence that doesn't fit on the screen.",0,330)
lcd.set_cursor(0,1)
lcd.write("hello world")

