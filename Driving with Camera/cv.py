import cv2
import numpy as np
import paho.mqtt.client as mqtt

# init mqtt client
# client = mqtt.Client("EddyElijahLEGO")
# client.connect('172.16.9.41', 1883)

# def send2Lego(coord):
#     client.publish('EETopic', str(coord))

# Function to get coordinate and draw lines and text
def draw_coordinate_info(image, coordinate):
    # Add text displaying coordinates
    cv2.putText(image, f"Coordinates: {coordinate}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Function to get coordinate of a point in an image with purple color
def get_purple_coordinate(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for purple color in HSV
    lower_purple = np.array([130, 50, 50])
    upper_purple = np.array([170, 255, 255])

    # Threshold the HSV image to get only purple colors
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables for the contour with the largest area
    max_contour = None
    max_area = 0

    # Iterate through contours
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        # Calculate the bounding box around the largest purple contour
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the centroid of the largest purple contour
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(image, (cX, cY), 5, (255, 0, 0), -1)
            return (cX, cY)

    return None

# Define a video capture object and start image
vid = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = vid.read()

        # Your image processing code here (modify as needed)
        coordinate = get_purple_coordinate(frame)

        if coordinate is not None:
            # send2Lego(coordinate)
            print("Coordinate:", coordinate)

        # Call the function to draw coordinate information
        draw_coordinate_info(frame, coordinate)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # Release the VideoCapture and close all windows on keyboard interrupt
    print('Keyboard interrupt')
finally:
    # Release the VideoCapture and close all windows
    vid.release()
    cv2.destroyAllWindows()
    # client.disconnect()
