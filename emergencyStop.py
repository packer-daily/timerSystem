import uasyncio as asyncio
from machine import Pin

# Pins
output = Pin(15, Pin.OUT)
estop = Pin(14, Pin.IN, Pin.PULL_UP)  # Active LOW

# Global flag
emergency_triggered = False

async def emergency_monitor():
    global emergency_triggered
    while True:
        if estop.value() == 0:  # Pressed
            print("EMERGENCY STOP TRIGGERED!")
            emergency_triggered = True
            output.off()
            # Wait until released
            while estop.value() == 0:
                await asyncio.sleep(0.1)
            print("E-Stop released.")
            emergency_triggered = False
        await asyncio.sleep(0.05)

async def timed_task(duration=10):
    while True:
        if not emergency_triggered:
            print("System Running...")
            output.on()
            for i in range(duration * 10):  # 10x per second
                if emergency_triggered:
                    print("Emergency during operation!")
                    break
                await asyncio.sleep(0.1)
            output.off()
            print("Cycle Complete.\nWaiting 5 seconds before next...")
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(0.5)

async def main():
    asyncio.create_task(emergency_monitor())
    await timed_task(10)

asyncio.run(main())
