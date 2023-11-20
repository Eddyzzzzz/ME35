# Import Libraries----------------------------------------------
from machine import ADC
import thermistor
import mqtt
import network
import machine
import struct, time
import requests
import utime
import time
from machine import Pin, UART

# Wifi Connection & Adafruit Dashboard Connection --------------
#ssid = 'tufts_eecs'
#passwd = 'foundedin1883'
#computerIP = '10.5.15.62'

ssid = 'Tufts_Wireless'
passwd = ''
#computerIP = '172.16.9.59'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,passwd)
while not station.isconnected():
    time.sleep(1)
print('Connection successful')
print(station.ifconfig())

mqttaio = mqtt.mqttAIO() # Adafruit Dashboard

# Define -------------------------------------------------------
adcpin = 27
sensor = ADC(adcpin) # Sensor

count = 200 # Timer for sending to dashboard
    
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    
#fred = mqtt.MQTTClient('Eddy', computerIP)
#fred.connect()
#fred.set_callback(whenCalled)
    
airtable_token = 'pataxw7zB3sqq4fr9.0029b03c6f2ad42be12afe43c9f354c0e63620819d2049880fbfa968f120d589'

fields = []

url = "https://api.airtable.com/v0/appglzCbSKhzw8eWW/tblYqkBUuEnN1lYX4/rec6XWBd1c5ZNwJVg"
headers = {
           'Authorization':f'Bearer {airtable_token}',
           'Content-Type':'application/json'
          }

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=2)

# Main Loop ----------------------------------------------------
    
while True:
    # Read Sensor
    adc = sensor.read_u16() 
    Vout = (3.3/65535)*adc
    TempC = thermistor.thermistorTemp(Vout)
    TempF = TempC * 1.8 + 32
    #print(round(TempC, 1) + ", " + round(TempF, 1))
    
    # Read Color
    reply = requests.request("GET", url, headers=headers)
    if reply.status_code == 200:
        reply = reply.json() # JSON array of info
        airtable_color = reply["fields"]["Temperature"]
        #print(airtable_color)
    
    # Send Dashboard
    if count == 200:
        mqttaio.send_temp(round(TempC * 1.8 + 32, 1), round(TempC, 1))
        count = 0;
        
    # Send to Screen
    msg = str(round(TempC, 1)) + " " + str(round(TempF, 1)) + " " + airtable_color 
    uart.write(msg)
    print (msg)
    
    count += 1
    time.sleep(1)
    
#fred.disconnect()
