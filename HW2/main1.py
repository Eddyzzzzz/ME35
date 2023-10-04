from machine import Pin,UART,PWM, I2C
import time, struct

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=2)

photoRes = machine.ADC(2)
amb = photoRes.read_u16() / 65536

yLed = PWM(Pin(13))
rLed = PWM(Pin(12))
bLed = PWM(Pin(11))
gLed = PWM(Pin(10))

YEL = 0
RED = 0
BLU = 0
GRE = 0
while True:
    li = photoRes.read_u16() / 65536
    realLi = int(65536 - (li*65536))
    print(realLi)
    light = uart.read()
    if light:
        light = light.decode()
    print(light)
    if (light == "A"):
        YEL = 1
        RED = 0
        BLU = 0
        GRE = 0
    elif (light == "B"):
        YEL = 0
        RED = 1
        BLU = 0
        GRE = 0
    elif (light == "x"):
        YEL = 0
        RED = 0
        BLU = 1
        GRE = 0
    elif (light == "y"):
        YEL = 0
        RED = 0
        BLU = 0
        GRE = 1
    yLed.duty_u16(YEL*realLi)
    rLed.duty_u16(RED*realLi)
    bLed.duty_u16(BLU*realLi)
    gLed.duty_u16(GRE*realLi)
    
    time.sleep(0.1)
