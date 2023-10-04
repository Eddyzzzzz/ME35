from machine import Pin, UART, PWM, I2C
import time, struct
import uasyncio as asyncio
import joystick
import acgy

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=2)

led = PWM(Pin(14, mode=Pin.OUT))
button = Pin(28, Pin.IN)
buzzer = PWM(Pin(22, mode=Pin.OUT))

yLed = Pin(13, Pin.OUT) 
rLed = Pin(12, Pin.OUT) 
bLed = Pin(11, Pin.OUT)
gLed = Pin(10, Pin.OUT)

#X button corresponds to bit 6
BTN_CONST = [1 << 6, 1 << 2, 1 << 5, 1 << 1, 1 << 0, 1 << 16]
BTN_Value = ['x','y','A','B','select','start']
BTN_Mask = 0
for btn in BTN_CONST:
    BTN_Mask |=  btn

joystick.digital_setup()
last_x, last_y, last_btn = 0,0,[False] * len(BTN_CONST)

[ax,ay,az] = acgy.readAc()
x = 1023 - joystick.read_joystick(14)
y = 1023 - joystick.read_joystick(15)
base = ay

async def sensorLoop():
    global buttons
    global last_btn
    global BTN_Value
    global x
    global y
    global ay
    while True:
        x = 1023 - joystick.read_joystick(14)
        y = 1023 - joystick.read_joystick(15)
        
        [ax,ay,az] = acgy.readAc()
        
        buttons = [ not joystick.digital_read() & btn for btn in BTN_CONST]
    
        whichBTN = ''
        for btn, last, name in zip(buttons,last_btn,BTN_Value):
            if (btn != last) and btn: #if it has changed and it is true
                if (name == "A"):
                    whichBTN = 'A'
                elif (name == "B"):
                    whichBTN = 'B'
                elif (name == "x"):
                    whichBTN = 'x'
                elif (name == "y"):
                    whichBTN = 'y'
        
        last_btn = buttons
        
        uart.write(whichBTN)
        #message = uart.read()
        #if message:
        #    print(message.decode('utf-8'))

        if  button.value():
            uart.write("JUST DANCE!!!")
            
        await asyncio.sleep(0.01)

async def ledLoop():
    while True:
        led.duty_u16(int(65025*(abs((ay-base)/20000))))

        await asyncio.sleep(0.01)

async def buzzerLoop():
    while True:
        buzzer.duty_u16(int(65025*y/1023))
        
        await asyncio.sleep(0.03*x/1023)
        
        buzzer.duty_u16(0)
        
        await asyncio.sleep(0.03*x/1023)

async def main(duration):
    loop = asyncio.new_event_loop()
    loop.create_task(sensorLoop())
    loop.create_task(ledLoop())
    loop.create_task(buzzerLoop())
    
    await asyncio.sleep(duration)
    
def test(duration):
    try:
        asyncio.run(main(duration)) #start everything running
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        asyncio.new_event_loop()  #end loop
        print('clear state')
        
test(800)
led.duty_u16(0)
buzzer.duty_u16(0)