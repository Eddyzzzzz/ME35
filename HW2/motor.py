import time
from machine import Pin

class servo():
    def __init__(self, gpio=15, start = 1.5):
        self.gpio = gpio
        self.pin = Pin(gpio, Pin.OUT)
        self.pos = self.run(start)
        
    def run(self, pos):
        up = int(pos * 1000)
        down = int(1/50 * 1000000 - up)
        self.pin.on()
        time.sleep_us(up)
        self.pin.off()
        time.sleep_us(down)

fred = servo(15)
buzzer = Pin(22, Pin.OUT)
buzzer.on()



        