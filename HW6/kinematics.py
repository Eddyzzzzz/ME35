import matplotlib.pyplot as plt
import math
import tinyik
import numpy as np

def generate_circle_coordinates(origin_x, origin_y, diameter, num_points):
    # Calculate the radius of the circle
    radius = diameter / 2.0
    
    # Initialize an empty list to store the coordinates
    coordinates = []
    
    # Calculate the angle increment between points on the circle
    angle_increment = 2 * math.pi / num_points
    
    # Generate coordinates for each point on the circle
    for i in range(num_points):
        # Calculate the angle for this point
        angle = i * angle_increment
        
        # Calculate the x and y coordinates
        x = origin_x + radius * math.cos(angle)
        y = origin_y + radius * math.sin(angle)
        
        # Append the coordinates as a tuple (x, y) to the list
        coordinates.append((x, y))
    
    return coordinates

# For the HW6 problem 
origin_x = 1.0   # X-coordinate of the origin
origin_y = 0.0   # Y-coordinate of the origin
diameter = 1.0   # Diameter of the circle
num_points = 100  # Number of points on the circle

circle_coordinates = generate_circle_coordinates(origin_x, origin_y, diameter, num_points)

# Extract x and y coordinates for plotting
x_coords, y_coords = zip(*circle_coordinates)

# Create a scatter plot of the circle coordinates
plt.scatter(x_coords, y_coords, marker='o', label='Circle Points')

# Set labels and title
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Circle Plot')

# Add a legend
plt.legend()

# Show the plot
plt.grid()

plt.show()

## Print the generated coordinates
#for i, (x, y) in enumerate(circle_coordinates):
#    print(f"Point {i + 1}: ({x}, {y})")

arm = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])
circle = []
for i in range(num_points):
    arm.ee = [x_coords[i], y_coords[i], 0.]
    npresult = np.round(np.rad2deg(arm.angles))
    result = [float(x) for x in npresult]
    circle.append(result)
    #print(result)

print(circle)
np.savetxt("circle.txt", circle)
    
