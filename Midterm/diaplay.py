import random
from machine import Pin, SPI
import gc9a01

import utime
import italicc

import vga1_bold_16x32 as font

from machine import Pin, UART
import time, struct


# Get the current time in UTC
# utc_time = time.localtime()

#------joystck pin declaration----- 
joyRight = Pin(17,Pin.IN)
joyDown  = Pin(18,Pin.IN)
joySel   = Pin(19,Pin.IN)
joyLeft  = Pin(20,Pin.IN)
joyUp    = Pin(21,Pin.IN)

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), bits=8, parity=None, stop=2)

spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(
    spi,
    240,
    240,
    reset=Pin(12, Pin.OUT),
    cs=Pin(9, Pin.OUT),
    dc=Pin(8, Pin.OUT),
    backlight=Pin(13, Pin.OUT),
    rotation=0)

tft.init()
tft.rotation(0)
tft.fill(gc9a01.BLACK)
utime.sleep(0.5)

tft.text(font, "Hello", 80, 100, gc9a01.WHITE)
#tft.draw(italicc, "hello" , 100, 50, gc9a01.BLUE)
#tft.fill_rect(120,120,200,200, gc9a01.BLUE)
#tft.pixel(100, 50, gc9a01.BLUE)

TC    = "0"
TF    = "0"
color = "none"

#timer
count = 0
state = False
tim   = ""

while True:

    if state:
        # Calculate minutes, seconds, and tenths of a second
        minutes = count // 600
        seconds = (count % 600) // 10
        tenths = count % 10
        tim = str(minutes) + ":" + str(seconds) + ":" + str(tenths)
        count += 1
          
    fred = uart.read()
    if fred:
        arr = fred.decode().split()
        print(arr)
        TC    = arr[0]
        TF    = arr[1] + " C"
        color = arr[2] + " F"
    
    if(joyRight.value() == 0):
        tft.fill(gc9a01.BLUE)

    elif(joyDown.value() == 0):
        tft.fill(gc9a01.RED)

    elif(joySel.value() == 0):
        tft.fill(gc9a01.GREEN)
        state = not state
        
    elif(joyLeft.value() == 0):
        tft.fill(gc9a01.CYAN)
   
    elif(joyUp.value() == 0):
        tft.fill(gc9a01.MAGENTA)
        
    if color == 'green':
        tft.text(font, TC, 80, 120, gc9a01.WHITE)
    else:
        tft.text(font, TF, 80, 120, gc9a01.WHITE)
            
    tft.text(font, tim, 80, 80, gc9a01.WHITE)
    if not state:
        count = 0
            
    time.sleep(0.1)



