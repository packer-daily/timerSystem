UNL PAT Lab Wind Tunnel Timer
=============================

Author: Packer Daily  
Version: Summer 2025  
Platform: Raspberry Pi Pico 2W  
Display: Grove I2C 16x2 LCD  
Input: 4x4 Keypad  
Control: GPIO output (MOSFET/relay controlled)  
Language: MicroPython (uasyncio)

--------------------------------------------------
PROJECT SUMMARY
--------------------------------------------------
This project provides a precision timer control box used for wind tunnel pesticide deposition trials in the UNL Pesticide Application Technology Lab. 

It allows researchers to:
- Set spray durations (supports decimal seconds)
- Start timed spray cycles with a single button press
- Cancel spray operations safely mid-run
- Trigger the spray system manually for testing or calibration

All functions are accessible from a Grove-compatible keypad and LCD screen, housed in a compact, lab-safe enclosure.

--------------------------------------------------
MAIN FEATURES
--------------------------------------------------
✔ Simple text interface via 16x2 Grove LCD  
✔ Adjustable spray time with decimal support  
✔ Run/Cancel cycle with visual and physical feedback  
✔ Manual mode for direct operator control  
✔ Non-blocking, async-based event handling  
✔ Emergency stop support (via D key)

--------------------------------------------------
INTERFACE OVERVIEW
--------------------------------------------------
[Main Menu]
1 - Run (Starts the saved spray time)
2 - Set Time (Enter new spray duration)
3 - More (Access manual mode and help)

[More Menu]
1 - Info (Scrolling help text)
2 - Manual (Press # to manually toggle spray)
3 - Back (Return to main menu)

[Special Keys]
# - Confirm input or toggle spray in Manual
. - Decimal point (used once per input)
D - Cancel / Emergency stop / Back

--------------------------------------------------
DEFAULT GPIO PINOUT
--------------------------------------------------
- LCD I2C: SDA = GP4, SCL = GP5  
- Keypad rows: GP6–GP9  
- Keypad cols: GP10–GP13  
- Output to spray device: GP16  
- Onboard LED used for spray feedback

--------------------------------------------------
KNOWN LIMITATIONS
--------------------------------------------------
- No persistent memory: spray time resets on power-off  
- No real-time clock or external trigger support  
- System assumes clean 5V input and hardware debounce

--------------------------------------------------
NOT IMPLEMENTED (INTENTIONALLY LEFT OUT)
--------------------------------------------------
The code contains a commented-out section for saving favorite spray durations (A, B, C). This feature was not part of the project scope and remains **untested**. It has been removed from active code to ensure system stability and clarity for future users.

--------------------------------------------------
FUTURE EXPANSION IDEAS
--------------------------------------------------
- Add EEPROM or file-based memory to support preset durations  
- Add external interrupt support for sync with wind tunnel controller  
- Upgrade to larger LCD or OLED for richer feedback  
- Add USB serial logging for automated experiment records

--------------------------------------------------
CONTACT / ATTRIBUTION
--------------------------------------------------
This project was developed by Packer Daily during a summer research position with the UNL PAT Lab. For technical questions, please refer to the annotated source code or speak with the lab PI or supervising engineer.


