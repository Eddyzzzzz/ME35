import time
import machine
import mqtt
import network, ubinascii
import Gamepad as GP
from machine import PWM
import urequests as requests

ssid = 'Tufts_Wireless'
passwd = ''
computerIP = '172.16.9.151'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,passwd)
while not station.isconnected():
    time.sleep(1)
print('Connection successful')
print(station.ifconfig())

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    
def readGP(gamePad):
    # Async function to read gamepad joystick input and turn the motor
    # in the corresponding direction using the Servo library
    x = str(gamePad.read_joystickX())
    y = str(gamePad.read_joystickY())
    #b = gamePad.read_buttons()
    #z = list(b.values())
    #z1 = [str(x) for x in z]
    #a = [x] + [y] + z1
    a = [x] + [y]
    result = ' '.join(a)
    print(result)
    return result

#X button corresponds to bit 6



fred = mqtt.MQTTClient('Eddy', computerIP)
fred.connect()
fred.set_callback(whenCalled)

#fred.subscribe('Pico/listen')
gamePad = GP.gamepad()
while True:
    #fred.check_msg() #check subscriptions - you might want to do this more often
    msg = readGP(gamePad)
    fred.publish('cybertruck',msg)
    readGP(gamePad)
    time.sleep(0.02)

fred.disconnect()
