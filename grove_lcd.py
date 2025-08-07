from machine import I2C, Pin
import time

class GroveLCD:
    def __init__(self, i2c, addr=0x3E):
        self.i2c = i2c
        self.addr = addr
        self.init_lcd()

    def cmd(self, byte):
        self.i2c.writeto(self.addr, b'\x00' + bytes([byte]))
        time.sleep_ms(1)

    def data(self, byte):
        self.i2c.writeto(self.addr, b'\x40' + bytes([byte]))
        time.sleep_ms(1)

    def init_lcd(self):
        time.sleep_ms(50)
        self.cmd(0x38)  # Function set: 8-bit, 2 line
        self.cmd(0x39)  # Function set: extended instruction
        self.cmd(0x14)  # Internal OSC frequency
        self.cmd(0x70)  # Contrast set (adjust lower 4 bits)
        self.cmd(0x56)  # Power/Icon/Contrast control
        self.cmd(0x6C)  # Follower control
        time.sleep_ms(200)
        self.cmd(0x38)  # Function set: normal instruction
        self.cmd(0x0C)  # Display ON, Cursor OFF
        self.clear()

    def clear(self):
        self.cmd(0x01)
        time.sleep_ms(2)

    def home(self):
        self.cmd(0x02)
        time.sleep_ms(2)

    def set_cursor(self, col, row):
        # 0x80 is line 1, 0xC0 is line 2
        address = 0x80 + (0x40 * row) + col
        self.cmd(address)

    def write(self, text):
        for char in text:
            self.data(ord(char))

    def write_line(self, text, row=0):
        self.set_cursor(0, row)
        self.write(text.ljust(16)[:16])  # Pad or truncate to 16 chars
