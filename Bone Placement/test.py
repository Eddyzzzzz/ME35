from http.server import BaseHTTPRequestHandler, HTTPServer
import time
hostName = "localhost"
serverPort = 8080
page = '''
<!DOCTYPE html>
<html>
<head><title>Rogers Slider</title>
<script>
function updateSliderPWM(element) {
      var sliderValue = document.getElementById("pwmSlider").value;
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "/slider?value="+sliderValue, true);
      xhr.send();
}</script>
</head>
<body>
<div id="slider_thing" class="tabcontent">
        <p><input type="range" oninput="updateSliderPWM(this)" id="pwmSlider" min="0" max="180" value="%SLIDERVALUE%" step="1" class="slider"></p>
</div>
</body></html>
'''
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page, "utf-8"))
        if '/slider' in self.path:
            print(self.path.split('=')[1])
            
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")