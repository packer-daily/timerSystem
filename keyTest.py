from machine import Pin
from keypad import Keypad
from time import sleep

led = Pin("LED", Pin.OUT)

rowPins = [Pin(6), Pin(7), Pin(8), Pin(9)]
colPins = [Pin(10), Pin(11), Pin(12), Pin(13)]

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['.', '0', '#', 'D']
]

keypad = Keypad(rowPins, colPins, keys)

while True:
    keyPressed = keypad.read_keypad()
    if keyPressed:
        print("Key Pressed:", keyPressed)
        if keyPressed == '#':
            led.toggle()

        # Wait for the key to be released
        while keypad.read_keypad() is not None:
            sleep(0.01)  # small delay to avoid busy loop
    sleep(0.05)  # polling delay to reduce CPU usage

