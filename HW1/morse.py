from machine import Pin, PWM
from utime import sleep
import uasyncio as asyncio

morseLed = Pin(15, Pin.OUT) #LED flashing morse name
morseLed.low()
photo_pin = machine.ADC(28) #analog reading for light sensor
lightLed = PWM(Pin(19)) # LED brightness based on light
lightLed.freq(1000)

TIME_UNIT = .2

# MORSE SETUP
morse_dict = {'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..'}

# morse timing rules: https://www.codebug.org.uk/learn/step/541/morse-code-timing-rules/
def dot(): #1 time unit + 1 btwn
    morseLed.on()
    sleep(TIME_UNIT)
    morseLed.off()
    sleep(TIME_UNIT)
    
def dash(): #2 time units
    morseLed.on()
    sleep(TIME_UNIT*2)
    morseLed.off()
    sleep(TIME_UNIT)
    
def pause(): # 2 time units
    sleep(TIME_UNIT*2)
    
# LIGHT SENSOR SETUP
def map(val, loval, hival, tolow, tohigh):
    if loval <= val <= hival:
        newval = (val - loval)/(hival-loval)*(tohigh-tolow) + tolow
        return int(newval)
    else:
        raise(ValueError)

#--------------------------#
 
# def light_val():
#     val = photo_pin.read_u16()
#     print(val)

async def photoLED():
    while True:
        val = photo_pin.read_u16()
        print(val)
        mapped_val = map(val, 0, 2000, 0, 65025)
        mapped_val *= 2
        lightLed.duty_u16(mapped_val)
        await asyncio.sleep_ms(100)
    
async def morse_name(name): #no spaces allowed in ur name
    while True:
        name = name.upper()
        for i in name:
            # need to iterate through morse of each letter
            print(i, ": ", morse_dict[i])
            for symbol in morse_dict[i]:
                if symbol == "-":
                    dash()
                    #photoLED()
                elif symbol == ".":
                    dot()
                    #photoLED()
                #pause()
        await asyncio.sleep_ms(1000)

name = input("What is your name? \n")
    
# Create asyncio tasks
loop = asyncio.get_event_loop()
loop.create_task(morse_name(name))
loop.create_task(photoLED())

# Start the event loop
loop.run_forever()

