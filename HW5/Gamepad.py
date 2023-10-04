from machine import Pin, I2C
import struct, time
import time

#i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)

ADC_BASE = 0x09
ADC_OFFSET = 0x07
GPIO_BASE = 0x01
GPIO_BULK = 0x04
GPIO_DIRCLR_BULK = 0x03
GPIO_PULLENSET = 0x0B
GPIO_BULK_SET = 0x05

#X button corresponds to bit 6
BTN_CONST = [1 << 6, 1 << 2, 1 << 5, 1 << 1, 1 << 0, 1 << 16]
BTN_Value = ['x','y','A','B','select','start']
BTN_Mask = 0
for btn in BTN_CONST:
    BTN_Mask |=  btn

class gamepad():

    def __init__(self, mode=0, sclPin=17, sdaPin=16):
        self.i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
        self.buttonPin = 4
        self.xWritePin = 14
        self.yWritePin = 15
        self.joyReadPin = 2
        self.GamePad = 0x50
        self.last_btn = [False] * len(BTN_CONST)


    def digital_setup(self):
        cmd = bytearray(4)
        cmd[0:] = struct.pack(">I", BTN_Mask)
        buffer = bytearray([GPIO_BASE, GPIO_DIRCLR_BULK]) + cmd
        reply = self.i2c.writeto(self.GamePad,buffer)
        buffer = bytearray([GPIO_BASE, GPIO_PULLENSET]) + cmd
        reply = self.i2c.writeto(self.GamePad,buffer)
        buffer = bytearray([GPIO_BASE, GPIO_BULK_SET]) + cmd
        reply = self.i2c.writeto(self.GamePad,buffer)

    def digital_read(self, delay=0.008):
        '''Get the values of all the pins on the "B" port as a bitmask'''
        buffer = bytearray([GPIO_BASE, GPIO_BULK])
        buf = self.i2c.writeto(self.GamePad,buffer)
        time.sleep(delay)
        buf = self.i2c.readfrom(self.GamePad,self.buttonPin)
        try:
            ret = struct.unpack(">I", buf)[0]
        except OverflowError:
            buf[0] = buf[0] & 0x3F
            ret = struct.unpack(">I", buf)[0]
        return ret & BTN_Mask

    def read_buttons(self):
        buttons = [ not self.digital_read() & btn for btn in BTN_CONST]
        for btn, last, name in zip(buttons,self.last_btn,BTN_Value):
            if (btn != last) and btn: #if it has changed and it is true
                print(name)
        self.last_btn = buttons
        #return dict(zip(BTN_Value, buttons))
        return buttons

    def read_joystickX(self):
        return 1023 - self.read_joystick(self.xWritePin)

    def read_joystickY(self):
        return 1023 - self.read_joystick(self.yWritePin)

    def read_joystick(self, pin, delay = 0.008):
        '''Read an analog signal from the game pad - define both the pin and a delay between write and read'''
        reply = self.i2c.writeto(self.GamePad,bytearray([ADC_BASE, ADC_OFFSET + pin]))
        time.sleep(delay)
        reply = self.i2c.readfrom(self.GamePad, self.joyReadPin)
        return struct.unpack('>H',reply)[0]