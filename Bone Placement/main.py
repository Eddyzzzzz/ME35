#!/usr/bin/env python3
import time
from http.server import HTTPServer
import paho.mqtt.client as mqtt 
import time
from flask import Flask, request, jsonify, Response
import os
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
import threading

# broker_address=''
# client = mqtt.Client("Eddy") 
# client.connect(broker_address)

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Controlled Ambulance</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            display: flex;
            align-items: center;
            text-align: center;
        }

        #joystick-container {
            width: 200px;
            height: 200px;
            background-color: #e0e0e0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        #joystick {
            width: 80px;
            height: 80px;
            background-color: #3498db;
            border-radius: 50%;
            position: absolute;
            cursor: pointer;
        }

        #button-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .button {
            width: 100px;
            height: 40px;
            background-color: #27ae60;
            color: #fff;
            font-size: 16px;
            margin: 10px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
        }

        .button:hover {
            background-color: #1e983b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="joystick-container">
            <div id="joystick"></div>
        </div>

        <form action="" method="get" class="form-example"></form>
        <div id="button-container">
            <button id="up-button" class="button">Up</button>
            <button id="down-button" class="button">Down</button>
            <button id="left-button" class="button">Left</button>
            <button id="right-button" class="button">Right</button>
            <div id="button-status">Button Status: </div>
            <div id="joystick-value">Joystick Value: X: 0.00, Y: 0.00</div>
        </div>

        <div id="slider_thing" class="tabcontent">
            <p><input type="range" oninput="updateSliderPWM(this)" id="pwmSlider" min="0" max="180" value="%SLIDERVALUE%" step="1" class="slider"></p>
        </div>

    </div>

<script>
    const joystick = document.getElementById('joystick');
    const upButton = document.getElementById('up-button');
    const downButton = document.getElementById('down-button');
    const leftButton = document.getElementById('left-button');
    const rightButton = document.getElementById('right-button');

    let joystickX = 0;
    let joystickY = 0;
    let button    = 'N';
    let send = ["0", "0", "N", "0"];

    function updateSliderPWM(element) {
        
        var sliderValue = document.getElementById("pwmSlider").value;
        var xhr = new XMLHttpRequest();
        send[3] = sliderValue;
        xhr.open("GET", "/send?value="+send, true);
        xhr.send();
    }

    // Function to update the displayed joystick value
    function updateJoystickValue() {
        document.getElementById('joystick-value').textContent = `Joystick X: ${joystickX.toFixed(2)}, Y: ${joystickY.toFixed(2)}`;
        
        var xhr = new XMLHttpRequest();
        send[0] = String(joystickX.toFixed(0));
        send[1] = String(joystickY.toFixed(0));
        xhr.open("GET", "/send?value="+send, true);
        xhr.send();
    }

    // Function to update button status
    function updateButtonStatus(status) {
        document.getElementById('button-status').textContent = status;
        var button = document.getElementById('button-status').textContent
        var xhr = new XMLHttpRequest();
        send[2] = button;
        xhr.open("GET", "/send?value="+send, true);
        xhr.send();
    }

    // Function to handle button release
    function handleButtonRelease() {
        updateButtonStatus('N');
    }

    // Add event listeners to control the joystick
    joystick.addEventListener('mousedown', (e) => {
        document.addEventListener('mousemove', moveJoystick);
        document.addEventListener('mouseup', releaseJoystick);
    });

    function moveJoystick(e) {
        const container = document.getElementById('joystick-container');
        const rect = container.getBoundingClientRect();
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const x = e.clientX - rect.left - centerX;
        const y = e.clientY - rect.top - centerY;

        const distance = Math.min(Math.sqrt(x * x + y * y), centerX);
        const angle = Math.atan2(y, x);

        joystickX = distance * Math.cos(angle);
        joystickY = distance * Math.sin(angle);
        
        

        joystick.style.transform = `translate(${joystickX}px, ${joystickY}px)`;
        updateJoystickValue();
        handleButtonRelease(); // Immediately update button status
    }

    function releaseJoystick() {
        document.removeEventListener('mousemove', moveJoystick);
        joystick.style.transform = 'translate(0, 0)';
        joystickX = 0;
        joystickY = 0;
        updateJoystickValue();
        handleButtonRelease(); // Immediately update button status
    }

    // Add event listeners for the up and down buttons
    upButton.addEventListener('mousedown', () => {
        // Implement your ambulance control logic here for moving up.
        updateButtonStatus('U');
    });

    upButton.addEventListener('mouseup', handleButtonRelease);

    downButton.addEventListener('mousedown', () => {
        updateButtonStatus('D');
    });

    downButton.addEventListener('mouseup', handleButtonRelease);

    leftButton.addEventListener('mousedown', () => {
        updateButtonStatus('L');
    });

    leftButton.addEventListener('mouseup', handleButtonRelease);

    rightButton.addEventListener('mousedown', () => {
        updateButtonStatus('R');
    });

    rightButton.addEventListener('mouseup', handleButtonRelease);

    // // Add keyboard event listeners
    // document.addEventListener('keydown', (e) => {
    //     e.preventDefault(); // Prevent default keyboard event
    //     switch (e.key) {
    //         case 'w':
    //             // Implement your logic for 'W' key press (e.g., moving up).
    //             upButton.mousedown();
    //             break;
    //         case 's':
    //             // Implement your logic for 'S' key press (e.g., moving down).
    //             downButton.mousedown();
    //             break;
    //         case 'a':
    //             // Implement your logic for 'A' key press (e.g., moving left).
    //             leftButton.mousedown();

    //             break;
    //         case 'd':
    //             // Implement your logic for 'D' key press (e.g., moving right).
    //             rightButton.mousedown();
    //             break;
    //     }
    // });

    // function sendDataToPython() {
    //     const data = {
    //         joystickX: joystickX,
    //         joystickY: joystickY,
    //         button: button
    //     };

    //     fetch('/update_data', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify(data)
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data.message);
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //     });
    // }

    // setInterval(sendDataToPython, 1000); // 1000 milliseconds (1 second)
</script>

</body>
</html>
'''

class Server(BaseHTTPRequestHandler):    

    # def infinite_loop():
    #     print('Some magic')
    #     threading.Timer(60, infinite_loop()).start()

    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # if request_extension == "" or request_extension == ".html":
        #     if self.path in routes:
        #         handler = TemplateHandler()
        #         handler.find(routes[self.path])
        #     else:
        #         handler = BadRequestHandler()
        # elif request_extension == ".py":
        #     handler = BadRequestHandler()
        # else:
        #     handler = StaticHandler()
        #     handler.find(self.path)
        # self.respond({
        #     'handler': handler
        # })

        self.wfile.write(bytes(page, "utf-8"))
        if '/send' in self.path:
            print("Send: " + self.path.split('=')[1])
        

        # self.wfile.write(bytes("<script>var xhttp = new XMLHttpRequest();xhttp.open('GET', send, true); xhttp.send();</script>", "utf-8"))
        # send = self.path
        # print(send)
        # time.sleep(1)  
        # infinite_loop()      
        # self.wfile.write(bytes("<script>var xhttp = new XMLHttpRequest();xhttp.open('GET', send, true); xhttp.send();</script>", "utf-8"))
        # client.publish("Eddy",send) 
        # time.sleep(0.2)

    # def handle_http(self, handler):
    #     status_code = handler.getStatus()
    #     self.send_response(status_code)
    #     if status_code == 200:
    #         content = handler.getContents()
    #         self.send_header('Content-type', handler.getContentType())
    #     else:
    #         content = "404 Not Found"
    #     self.end_headers()
    #     return bytes(content, 'UTF-8')

    # def respond(self, opts):
    #     response = self.handle_http(opts['handler'])
    #     self.wfile.write(response)


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))


