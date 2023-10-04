import network
import time
import network
import ubinascii
import urequests as requests


station = network.WLAN(network.STA_IF)
station.active(True)

ssid = 'Tufts_Wireless'
password = ''

station.connect(ssid, password)
while station.isconnected() == False:
    time.sleep(1)
    pass
print('Connection successful')
reply = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")
print(reply.json()['datetime'] if reply.status_code == 200 else 'Error')