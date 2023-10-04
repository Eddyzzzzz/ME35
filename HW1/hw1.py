# Write your code here :-)
from machine import Pin
import utime
led = Pin(15, Pin.OUT)
led.low()
photo_pin = machine.ADC(28)

TIME_UNIT = .3

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
    led.on()
    utime.sleep(TIME_UNIT)
    led.off()
    utime.sleep(TIME_UNIT)

def dash(): #2 time units
    led.on()
    utime.sleep(TIME_UNIT*2)
    led.off()
    utime.sleep(TIME_UNIT)

def pause(): # 2 time units
    utime.sleep(TIME_UNIT*2)


#x = morse_dict["L"]
# print(x)
# print(type(x))
# print(x[1])

def light_val():
    val = photo_pin.read_u16()
    print(val)

def morse_name(name): #no spaces allowed in ur name
    name = name.upper()
    for i in name:
        # need to iterate through morse of each letter
        print(i, ": ", morse_dict[i])
        for symbol in morse_dict[i]:
            if symbol == "-":
                dash()
                light_val()
            elif symbol == ".":
                dot()
                light_val()
            pause()


name = input("What is your name? \n")
morse_name(name)
