import numpy as np
import matplotlib.pyplot as plt

# Data
real_distance = np.array([36, 41, 46, 51, 56, 61, 66, 76])
lidar_distance = np.array([33, 38, 43, 48, 53, 58, 64, 69])
ultrasonic_distance = np.array([39, 43, 48, 53, 58, 62, 68, 78])

# Plotting
plt.figure(figsize=(6, 4))

plt.scatter(real_distance, lidar_distance, color='blue', label='Lidar')
plt.scatter(real_distance, ultrasonic_distance, color='red', label='Ultrasonic')

# Linear extrapolation
m_lidar, b_lidar = np.polyfit(real_distance, lidar_distance, 1)
m_ultrasonic, b_ultrasonic = np.polyfit(real_distance, ultrasonic_distance, 1)

x_values = np.linspace(30, 80, 100)
plt.plot(x_values, m_lidar * x_values + b_lidar, '--', color='blue', label='Lidar Linear Fit', linewidth=2)
plt.plot(x_values, m_ultrasonic * x_values + b_ultrasonic, '--', color='red', label='Ultrasonic Linear Fit', linewidth=2)

plt.xlabel('Real Distance [cm]')
plt.ylabel('Measured Distance [cm]')
plt.title('Measured distances of Lidar and Ultrasonic sensors')
plt.legend()
plt.grid(True)
plt.show()