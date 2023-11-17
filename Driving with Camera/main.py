# main.py
from BLE_CEEO import Yell, Listen
import time
import mqtt
import network, ubinascii
from machine import PWM
import urequests as requests

# computer to pico through mqtt 
ssid = 'Tufts_Wireless'
passwd = ''
computerIP = '172.16.9.41'

message = 's'

# connect mqtt
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,passwd)
while not station.isconnected():
    time.sleep(1)
print('Connection successful')
print(station.ifconfig())

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    global message
    message = msg.decode() 

# BLE peripheral
# def peripheral(name, message): 
try:
    # mqtt
    fred = mqtt.MQTTClient('Eddy', computerIP)
    fred.connect()
    fred.set_callback(whenCalled)
    fred.subscribe('EETopic')
    # BLE
    p = Yell('Eli', verbose = False)
    if p.connect_up():
        print('P connected')
        while True:
            fred.check_msg() #check subscriptions
            time.sleep(0.1)
            p.send(message)
                
            if p.is_any:
                print(p.read())
                
            if not p.is_connected:
                print('lost connection')
                break
            time.sleep(0.1)
            
except Exception as e:
    print(e)
finally:
    p.disconnect()
    fred.disconnect()
    print('closing up')
    
# peripheral('Eli', message)



