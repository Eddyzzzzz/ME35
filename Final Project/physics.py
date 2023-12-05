# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.optimize import curve_fit

# # Assuming you have the data in two lists width_data and transmission_data for two energy values

# # Data for total energy value 1
# width_data_1 = [1, 0.5, 1.5, 0.7, 0.3]  # Replace with your actual data
# transmission_data_1 = [0.06, 0.31, 0.01, 0.16, 0.58]  # Replace with your actual data

# # Data for total energy value 2
# width_data_2 = [1, 0.5, 1.5, 0.7, 0.3]  # Replace with your actual data
# transmission_data_2 = [0.03, 0.24, 0.00, 0.10, 0.54]  # Replace with your actual data
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Assuming you have the data in two lists width_data and transmission_data for two energy values

# Data for total energy value 1
width_data_1 = [0.3, 0.5, 0.7, 1, 1.5]  # Replace with your actual data
transmission_data_1 = [0.58, 0.31, 0.16, 0.06, 0.01]  # Replace with your actual data

# Data for total energy value 2
width_data_2 = [0.3, 0.5, 0.7, 1, 1.5]  # Replace with your actual data
transmission_data_2 = [0.54, 0.24, 0.10, 0.03, 0.01]  # Replace with your actual data

# Fit linear curves for both energy values
def linear_func(x, a, b):
    return a * x + b

popt_1, _ = curve_fit(linear_func, width_data_1, np.log(transmission_data_1))
popt_2, _ = curve_fit(linear_func, width_data_2, np.log(transmission_data_2))

# Plotting T vs. width on linear scale for energy 1
plt.figure(figsize=(8, 6))
plt.plot(width_data_1, transmission_data_1, 'o-', label='Energy 1')
plt.xlabel('Width (w)')
plt.ylabel('Transmission (T)')
plt.title('Transmission vs. Width (Linear Scale) - Energy 1')
plt.legend()
plt.grid(True)
plt.show()

# Plotting T vs. width on linear scale for energy 2
plt.figure(figsize=(8, 6))
plt.plot(width_data_2, transmission_data_2, 's-', label='Energy 2')
plt.xlabel('Width (w)')
plt.ylabel('Transmission (T)')
plt.title('Transmission vs. Width (Linear Scale) - Energy 2')
plt.legend()
plt.grid(True)
plt.show()

# Plotting T vs. width on logarithmic scale with linear fits for energy 1
plt.figure(figsize=(8, 6))
plt.semilogy(width_data_1, transmission_data_1, 'o-', label='Energy 1')
plt.plot(width_data_1, np.exp(linear_func(np.array(width_data_1), *popt_1)), '--', label='Fit Energy 1')
plt.xlabel('Width (w)')
plt.ylabel('Transmission (T)')
plt.title('Transmission vs. Width (Log-Linear Scale with Linear Fit) - Energy 1')
plt.legend()
plt.grid(True)
plt.show()

# Plotting T vs. width on logarithmic scale with linear fits for energy 2
plt.figure(figsize=(8, 6))
plt.semilogy(width_data_2, transmission_data_2, 's-', label='Energy 2')
plt.plot(width_data_2, np.exp(linear_func(np.array(width_data_2), *popt_2)), '--', label='Fit Energy 2')
plt.xlabel('Width (w)')
plt.ylabel('Transmission (T)')
plt.title('Transmission vs. Width (Log-Linear Scale with Linear Fit) - Energy 2')
plt.legend()
plt.grid(True)
plt.show()
