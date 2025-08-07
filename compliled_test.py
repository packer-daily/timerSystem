from machine import Pin, I2C
from keypad import Keypad
from time import sleep
from grove_lcd import GroveLCD

led = Pin("LED",Pin.OUT)

rowPins = [Pin(6), Pin(7), Pin(8), Pin(9)]
colPins = [Pin(10), Pin(11), Pin(12), Pin(13)]

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['.', '0', '#', 'D']
]

keypad = Keypad(rowPins, colPins, keys)

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = GroveLCD(i2c)

def getPulse():
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.set_cursor(0,1)
    num = ""
    while True:
        newKey = keypad.read_keypad()
        if newKey:
            if newKey != '#':
                lcd.write(newKey)
                num = num+newKey
                while keypad.read_keypad() is not None:
                    sleep(0.01)
            else:
                break
        sleep(0.05)
    print("Our stored num:",num)
    return float(num)

lcd.clear()
lcd.set_cursor(0,0)
lcd.write("Hello World!")
lcd.set_cursor(0,1)
lcd.write("RP2040 + Grove")
sleep(3)
lcd.clear()
lcd.set_cursor(0,0)
script = ""
state_case = 0
pulse = 0

while True:
    keyPressed = keypad.read_keypad()
    if keyPressed:
        script = script + keyPressed
        if keyPressed == '#':
            lcd.scroll_text(script)
        # Wait for the key to be released
        while keypad.read_keypad() is not None:
            sleep(0.01)  # small delay to avoid busy loop
    sleep(0.05)  # polling delay to reduce CPU usage
    while True:
        if state_case == 0:
            pulse = getPulse()
            state_case = 1
        else:
            led.toggle()
            sleep(pulse)
            led.toggle()
            state_case = 0
