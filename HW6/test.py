import time
import machine
import mqtt
import network, ubinascii
from machine import PWM
import urequests as requests

ssid = 'tufts_eecs'
passwd = 'foundedin1883'
computerIP = '10.5.15.62'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,passwd)
while not station.isconnected():
    time.sleep(1)
print('Connection successful')
print(station.ifconfig())

circle = ((-0.0, -0.0), (-40.0, 83.0), (-39.0, 83.0), (-38.0, 83.0), (-37.0, 84.0), (-36.0, 84.0), (-35.0, 85.0), (-34.0, 86.0), (-34.0, 86.0), (-33.0, 87.0), (-32.0, 88.0), (-32.0, 89.0), (-31.0, 91.0), (-31.0, 92.0), (-30.0, 93.0), (-30.0, 95.0), (-30.0, 96.0), (-29.0, 98.0), (-29.0, 99.0), (-29.0, 101.0), (-29.0, 103.0), (-29.0, 105.0), (-29.0, 106.0), (-29.0, 108.0), (-29.0, 110.0), (-29.0, 112.0), (-30.0, 114.0), (-30.0, 116.0), (-31.0, 118.0), (-31.0, 120.0), (-32.0, 122.0), (-32.0, 124.0), (-33.0, 126.0), (-34.0, 128.0), (-35.0, 130.0), (-36.0, 132.0), (-37.0, 134.0), (-39.0, 136.0), (-41.0, 138.0), (-42.0, 139.0), (-44.0, 141.0), (-47.0, 143.0), (-49.0, 144.0), (-52.0, 146.0), (-55.0, 147.0), (-58.0, 148.0), (-61.0, 149.0), (-65.0, 150.0), (-68.0, 151.0), (-72.0, 151.0), (-76.0, 151.0), (-79.0, 151.0), (-82.0, 151.0), (-85.0, 150.0), (-88.0, 149.0), (-91.0, 148.0), (-93.0, 147.0), (-94.0, 146.0), (-95.0, 144.0), (-96.0, 143.0), (-97.0, 141.0), (-97.0, 139.0), (-97.0, 138.0), (-97.0, 136.0), (-96.0, 134.0), (-96.0, 132.0), (-95.0, 130.0), (-94.0, 128.0), (-93.0, 126.0), (-92.0, 124.0), (-90.0, 122.0), (-89.0, 120.0), (-87.0, 118.0), (-86.0, 116.0), (-84.0, 114.0), (-83.0, 112.0), (-81.0, 110.0), (-79.0, 108.0), (-77.0, 106.0), (-76.0, 105.0), (-74.0, 103.0), (-72.0, 101.0), (-70.0, 99.0), (-68.0, 98.0), (-66.0, 96.0), (-65.0, 95.0), (-63.0, 93.0), (-61.0, 92.0), (-59.0, 91.0), (-58.0, 89.0), (-56.0, 88.0), (-54.0, 87.0), (-53.0, 86.0), (-51.0, 86.0), (-50.0, 85.0), (-48.0, 84.0), (-47.0, 84.0), (-45.0, 83.0), (-44.0, 83.0), (-43.0, 83.0))

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))

fred = mqtt.MQTTClient('Eddy', computerIP)
fred.connect()
fred.set_callback(whenCalled)

#fred.subscribe('Pico/listen')


#fred.check_msg() #check subscriptions - you might want to do this more often
for i in range(len(circle)):
    msg = str(circle[i])
    fred.publish('test',msg)
    time.sleep(0.1)

fred.disconnect()
