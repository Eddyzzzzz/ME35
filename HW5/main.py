import GamepadLib as GP
import AccelLib as AL
from ServoClass import Servo
from machine import PWM
import uasyncio as asyncio
import time
import urequests as requests
import network
import ubinascii

# Inspired by Tristan, thx buddy
# Global constants- mostly relating to API navigation, and a boolean to
#                   switch between home and Tufts wifi
atHome = False

allFeedUrl = 'https://io.adafruit.com/api/v2/Eddyzzz/feeds' 
headers = {'X-AIO-Key':APIkey,'Content-Type':'application/json'}
feedFormat = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data'
accelValueList = []
ratio = 10
accelDelay = 0.05

def wifiConnect():
    # Connect the pico to the local wifi
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if atHome:
        ssid = ''
        password = ''
    else:
        ssid = 'Tufts_Wireless'
        password = ''
    station.connect(ssid, password)
    while not station.isconnected():
        time.sleep(1)
        pass
    print('Wifi Connection successful')
    print(station.ifconfig())
    return station

def APIConnect():
    # Establish a connection with my API and save the feed names and IDs
    username = "Eddyzzz"
    APIkey = "aio_pNzg632KpO5gwAO3EvT54elJCqHm"
    reply = requests.get(allFeedUrl,headers=headers)
    if reply.status_code == 200:
        print("API Connection Succesful")
        reply = reply.json() #a JSON array of info
        keys = [x['key'] for x in reply]
        groups = [x['group']['name'] for x in reply]
        names = [x['name'] for x in reply]
        values = [x['last_value'] for x in reply]
        ids = [x['id'] for x in reply]
        print(names)
        print(ids)
        return dict(zip(names[0:3], ids[0:3]))
    else:
        print("API Connection failed")
        return None
    
def readAccel(accel, mode, axis):
    # Read the specified data from the accelerometer
    directs = {"x":0, "y":1, "z":2}
    if mode == "acc": # Accelerometer data
        return accel.allAccel()[directs[axis]]
    elif mode == "gyr":
        return accel.allGyro()[directs[axis]]
    else:
        print("Invalid accelerometer mode")
        return
    
def logData(url, data):
    # Post the given data to the given url
    reply = requests.post(url,headers=headers,json=data)  # reply is a requests.Response() object
    return reply

def uploadAccel(value, mode, axis, idDict):
    # Wrapper function to format and post accelerometer data to the right feed
    name = mode[0] + "_" + axis
    url = feedFormat % (username, idDict[name])
    data = {'value':value}
    reply = logData(url, data)
    print("accelPost:", value)
    return reply

async def measureAC(accel, mode, axis):
    # Async function to obtain and record accelerometer data
    global accelValueList
    while True:
        value = readAccel(accel, mode, axis)
        accelValueList.append(value)
        await asyncio.sleep(accelDelay)
        
async def postAC(idDict, mode, axis):
    # Async function to post the accel data to the dashboard
    # When this is included in the taskloop, everything slows down :(
    listIndex = 0
    while True:
        if listIndex < len(accelValueList):
            accelVal = accelValueList[listIndex]
            reply = uploadAccel(accelVal, mode, axis, idDict)
            reply.close()
            listIndex += ratio
            await asyncio.sleep(accelDelay * ratio)
        else:
            await asyncio.sleep(int(accelDelay * ratio / 2))
            
async def readGP(gamePad, motor):
    # Async function to read gamepad joystick input and turn the motor
    # in the corresponding direction using the Servo library
    lastX = 0
    neutral = 532
    motorMax = 1024
    motorPos = 512
    while True:
        x = gamePad.read_joystickX()
        if x > neutral:
            # Turn right
            motorPos = (motorPos - 2) % motorMax
            motor.goto(motorPos)
        elif x < neutral:
            # Turn left
            motorPos = (motorPos + 2) % motorMax
            motor.goto(motorPos)
        else:
            # Freeze
            motorPos = 512
            motor.middle()
            await asyncio.sleep_ms(1)
        lastX = x
        
async def bigLoop(idDict, timeLimit):
    # The main async loop which initializes the classes and starts the tasks
    accel = AL.accelerometer(1, 3, 2)
    gamePad = GP.gamepad()
    motor = Servo(12)
    mode = "gyr"
    axis = "z"
    print("beginning loop")
    asyncio.create_task(readGP(gamePad, motor))
    asyncio.create_task(measureAC(accel, mode, axis))
    asyncio.create_task(postAC(idDict, mode, axis))
    await asyncio.sleep(timeLimit)
    motor.deinit()
    print("Gyro Values:", accelValueList)
    
def main():
    # The final main function, gets everything set up and runs the loop
    station = wifiConnect()
    idDict = APIConnect()
    if idDict is None:
        print("API Connection Failed")
        return
    timeLimit = 30  # time in seconds
    try:
        asyncio.run(bigLoop(idDict, timeLimit))
    except KeyboardInterrupt:
        print("Keyboard interruption")
    finally:
        asyncio.new_event_loop()
        print('Loop finished, clear state')
main()