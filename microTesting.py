import _thread
from machine import Pin
import utime
import monitor

# --------- Core 1 Task (blinking LED) ----------
def blink_led():
    led = Pin("LED", Pin.OUT)
    while True:
        led.toggle()
        utime.sleep(0.5)
        print("hello from back up core")

# Start the second core
_thread.start_new_thread(blink_led, ())

# --------- Core 0 State Machine ----------
def state_idle():
    print("State: IDLE")
    utime.sleep(2)
    return "RUNNING"

def state_running():
    print("State: RUNNING")
    monitor.run()
    return "DONE"

def state_done():
    print("State: DONE")
    utime.sleep(2)
    return None  # Ends the FSM

# Dictionary-based FSM
fsm = {
    "IDLE": state_idle,
    "RUNNING": state_running,
    "DONE": state_done,
}

# Initial state
state = "IDLE"

# FSM loop on Core 0
while state:
    state = fsm[state]()
