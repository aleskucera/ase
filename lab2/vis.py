import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Data from the table
U_fan = np.array([3.5, 4, 5, 6, 7, 8, 9, 10])
U_br = np.array([0.12, 0.137, 0.165, 0.186, 0.203, 0.215, 0.215, 0.215])
U_sens = np.array([0.429, 0.435, 0.4425, 0.4484, 0.4534, 0.4564, 0.4566, 0.4568])

# Convert U_fan to Q_m
Q_v = (2.43 * U_fan - 4.81) * 10**(-4)  # m^3/s
Q_m = 1.293 * Q_v  # kg/s

# Define a formatter function to multiply tick labels by 10^3
def formatter(x, pos):
    return '{:.2f}'.format(x * 1000)

# Plotting Q_m for U_br
plt.figure(figsize=(7, 5))
plt.plot(Q_m, U_br, marker='o', color='blue', linewidth=2)
plt.xlabel('$Q_m$ [$10^{-3}$ kg/s]', fontsize=14)
plt.ylabel('$U_{br}$ [V]', fontsize=14)
# plt.title('Voltage $U_{br}$ vs Mass Flow Rate $Q_m$', fontsize=16)
plt.grid(True)

# Apply the custom formatter to the x-axis
plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))

plt.show()

# Plotting Q_m for U_sens
plt.figure(figsize=(7, 5))
plt.plot(Q_m, U_sens, marker='s', color='red', linewidth=2)
plt.xlabel('$Q_m$ [$10^{-3}$ kg/s]', fontsize=14)
plt.ylabel('$U_{sens}$ [V]', fontsize=14)
# plt.title('Voltage $U_{sens}$ vs Mass Flow Rate $Q_m$', fontsize=16)
plt.grid(True)

# Apply the custom formatter to the x-axis
plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))

plt.show()
