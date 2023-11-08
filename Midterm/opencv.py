import numpy as np

cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
image_to_analyze = cv2_image
b,g,r = cv2.split(cv2_image)
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY)

def find_largest_color_contour(lower, upper, color):
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image_to_analyze, lower, upper)
    output = cv2.bitwise_and(image_to_analyze, image_to_analyze, mask=mask)
    
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, (0,0,255), 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        if color == "red":
            # draw the biggest contour (c) in Red
            cv2.rectangle(output,(x,y),(x+w,y+h),(255,0,0),2)
        else:
            # draw the biggest contour (c) in Green
            cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

    # show the images
    display(Image.fromarray((np.hstack([cam.raw_image, output]))))

    # Return area of the biggest contour
    return w*h

# Find Largest Green
lower_g = [20, 80, 20]
upper_g = [140, 255, 90]
area_g = find_largest_color_contour(lower_g, upper_g, "green")
    
# Find Largest Red
lower_r = [20, 20, 120]
upper_r = [110, 100, 255]
area_r = find_largest_color_contour(lower_r, upper_r, "red")

largest_color = ""

if (area_g == area_r):
    display("[RESULT] Both colors are the same size.")
    largest_color = "n/a"
elif (area_g > area_r):
    display("[RESULT] The green object is larger.")
    largest_color = "green"
else:
    display("[RESULT] The red object is larger.")
    largest_color = "red"



import requests
import json

airtable_token = ''

fields = []

url = "https://api.airtable.com/v0/appglzCbSKhzw8eWW/tblYqkBUuEnN1lYX4/rec6XWBd1c5ZNwJVg"
headers = {
           'Authorization':f'Bearer {airtable_token}',
           'Content-Type':'application/json'
          }

update_data = {
                  "fields": {
                      "Temperature": f"{largest_color}"
                  }
              }

reply = requests.request("PATCH", url, headers=headers, data=json.dumps(update_data))
display('Sent!')

reply = requests.request("GET", url, headers=headers)
display(reply.status_code)
if reply.status_code == 200:
    reply = reply.json() # JSON array of info
    display("Read!")
    display(reply)
    airtable_color = reply["fields"]["Temperature"]
    display(f"Color from AirTable: {airtable_color}")

