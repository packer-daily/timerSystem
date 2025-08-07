# Libraries
import uasyncio as asyncio
from machine import Pin, I2C
from keypad import Keypad
from grove_lcd import GroveLCD
import json

# Global Variables
tag = 1
dec_tag = 1
state = 'a'
num = ""
saved = 0
#sav1 = load_config('A')
#sav2 = load_config('B')
#sav3 = load_config('C')

# Pin Formatting

led = Pin("LED",Pin.OUT)
switch = Pin(16,Pin.OUT)

helpText = "Use * for . Use # for enter Use D for back Set time changes how long the timer is on Run starts the timer for the set time Manual runs the timer when the # is pressed"

rowPins = [Pin(6), Pin(7), Pin(8), Pin(9)]
colPins = [Pin(10), Pin(11), Pin(12), Pin(13)]

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = GroveLCD(i2c)

# Structure Formatting

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['.', '0', '#', 'D']
]

keypad = Keypad(rowPins,colPins,keys)

# Async functions for individual states *PS this comment is on line 42 (;*

async def getPulse():
    global state, num, dec_tag, saved
    print("Getting pulse duration")
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.write("Input Spray Time")
    lcd.set_cursor(0,1)
    dec_tag = 1
    while True:
        newKey = keypad.read_keypad()
        if newKey:
            if newKey != '#':
                if newKey.isdigit():
                    lcd.write(newKey)
                    num = num+newKey
                    while keypad.read_keypad() is not None:
                        await asyncio.sleep(0.01)
                elif newKey == '.':
                    if dec_tag:
                        lcd.write(newKey)
                        num = num+newKey
                        dec_tag = 0
                elif newKey == 'D':
                    num = ""
                    state = 'b'
                    return
            else:
                break
        await asyncio.sleep(0.05)
    saved = float(num)
    num = ""
    state = 'b'

async def basicMenu():
    global state
    print("Basic menu active")
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.write("1 Run")
    lcd.set_cursor(6,0)
    lcd.write("2 Set time")
    lcd.set_cursor(0,1)
    lcd.write("3 More")
    while True:
        # Simulate menu check
        # print("Waiting for button press in menu...")
        newKey = keypad.read_keypad()
        if newKey == '1':
            state = 'c'
            await asyncio.sleep(0.5)
            break
        elif newKey == '2':
            state = 'a'
            await asyncio.sleep(0.5)
            break
        elif newKey == '3':
            state = 'd'
            await asyncio.sleep(0.5)
            break

async def startExp():
    global state, tag
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.write("D to cancel")
    stop_event = asyncio.Event()
    led.toggle()
    switch.toggle()
    tag = 1
    await asyncio.gather(
        runSpray(stop_event),
        checkButtons(stop_event)
)
    switch.toggle()
    led.toggle()
    print("Experiment Complete")
    state = 'b'
    return

async def runSpray(stop_event):
    global saved, state, tag
    print("Sprayer running...")
    count = 0
    while count < saved and not stop_event.is_set():
        # Simulate wind tunnel operation
        count += .01
        if count % 1 < .01:
            # print("Spraying...")
            lcd.set_cursor(0,1)
            script = str(int(count))
            lcd.write(script)
            lcd.write("   ")
        await asyncio.sleep(0.009)
    stop_event.set()
    tag = 0
    return

async def bigMenu():
    global state
    print("Big menu active")
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.write("1 Info")
    lcd.set_cursor(7,0)
    lcd.write("2 Manual")
    lcd.set_cursor(0,1)
    lcd.write("3 Back")
    #lcd.set_cursor(7,1)
    #lcd.write("4 Saved")
    while True:
        # Simulate big menu
        newKey = keypad.read_keypad()
        if newKey:
            print(newKey)
        if newKey == '1':
            state = 'f'
            await asyncio.sleep(0.5)
            break
        elif newKey == '2':
            state = 'e'
            await asyncio.sleep(0.5)
            break
        elif newKey == '3':
            await asyncio.sleep(0.5)
            state = 'b'
            break
        #elif newKey == '4':
            #state = 'g'
            #await asyncio.sleep(0.5)
            #break
        elif newKey == 'D':
            state = 'b'
            await asyncio.sleep(0.5)
            break
    print(state)
        #print("In big menu...")

async def manualMode():
    global state
    print("Manual mode")
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.write("# to spray")
    lcd.set_cursor(0,1)
    lcd.write("D to cancel")
    while True:
        # Manual control loop
        newKey = keypad.read_keypad()
        if newKey == '#':
            switch.toggle()
            led.toggle()
            while keypad.read_keypad() == '#':
                await asyncio.sleep(0.1)
            await asyncio.sleep(0.2)
            switch.toggle()
            led.toggle()
        elif newKey == 'D':
            state = 'd'
            await asyncio.sleep(.5)
            break
        await asyncio.sleep(0.1)

async def infoFull():
    global state
    stop_event = asyncio.Event()
    await asyncio.gather(
        displayInfo(helpText, stop_event),
        watchKey(stop_event)
    )
    state = 'd'

    
async def displayInfo(helpText, stop_event, row=0, delay=0.5):
    text = " " * 16 + helpText + " " * 16
    i = 0
    lcd.clear()
    lcd.set_cursor(0, 1)
    lcd.write("Press D to exit")
    while not stop_event.is_set():
        try:
            lcd.set_cursor(0, 0)
            lcd.write(text[i:i+16])
        except Exception as e:
            print("Scroll error:", e)
        await asyncio.sleep(delay)
        i = (i + 1) % (len(text) - 15)
        
async def watchKey(stop_event):
    print("Watching for back key...")
    while not stop_event.is_set():
        key = keypad.read_keypad()
        if key == 'D':
            print("Back key pressed.")
            stop_event.set()
            return
        await asyncio.sleep(0.05)

async def checkButtons(stop_event):
    global tag, saved
    print("Button checker running...")
    while not stop_event.is_set():
        # Check the emergency stop button
        newKey = keypad.read_keypad()
        if newKey == 'D':
            stop_event.set()
            saved = 0
            break
        await asyncio.sleep(0.001)


# Extra feature. Unfinished development. Explore at your own risk
#async def makeFavorite():
#    global tag
#    print("In make favorite")
#    lcd.clear()
    #lcd.set_cursor(0,0)
    #lcd.write("A B or C to save")
    #num = 0
    #while True:
#        newKey = keypad.read_keypad()
#        if newKey:
#            if newKey != 'A' or newKey != 'B' or newKey != 'C':
#                if newKey.isdigit():
#                    lcd.write(newKey)
#                    num = num+newKey
#                    while keypad.read_keypad() is not None:
#                        await asyncio.sleep(0.01)
#                elif newKey == '.':
#                    if tag:
#                        lcd.write(newKey)
#                        num = num+newKey
#                        tag = 0
#                elif newKey == 'D':
#                    tag = 1
#                    state = 'b'
#                    return
#            else:
#                tag = 1
#                save_config(newKey,num)
#                break
            
#def save_config(sec,value):
    #with open("config.json","w") as f:
        #json.dump({sec: value},f)
        
#def load_config(sec):
    #try:
        #with open("config.json","w") as f:
            #return json.load(f)[sec]
        #except:
            #return 1.0

# Dictionary monitoring the state
currentState = {
    'a': getPulse,
    'b': basicMenu,
    'c': startExp,
    'd': bigMenu,
    'e': manualMode,
    'f': infoFull,
    #'g': makeFavorite
}

# Main loop — must call and await the correct function
async def main():
    global state
    global count
    while True:
        handler = currentState.get(state)
        if handler:
            await handler()  # Await the coroutine from the dictionary
        else:
            print("Invalid state.")
            await asyncio.sleep(1)

# Start the asyncio event loop
asyncio.run(main())


