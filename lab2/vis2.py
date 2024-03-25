import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import FuncFormatter

# Data from the table
U_fan = np.array([3.5, 4, 5, 6, 7, 8, 9, 10])
U_VCC = np.array([8, 8.37, 8.83, 9.18, 9.51, 9.73, 9.74, 9.74])
U_sens = np.array([0.492, 0.509, 0.537, 0.557, 0.577, 0.592, 0.593, 0.592])

# Convert U_fan to Q_m
Q_v = (2.43 * U_fan - 4.81) * 10**(-4)  # m^3/s
Q_m = 1.293 * Q_v  # kg/s

# Convert U_sens to I
I = U_sens / 10  # Amperes

# Use only the first 6 values for fitting
Q_m_fit = Q_m[:6]
I_squared_fit = (I[:6])**2

# Compute square of I and sqrt of Q_m for fitting
Q_sqrt_fit = np.sqrt(Q_m_fit)

# Define linear function for estimation
def linear_function(x, a, b):
    return a + b * x

def formatter(x, pos):
    return '{:.1f}'.format(x * 1000)

# Perform least squares fitting
params, cov = curve_fit(linear_function, Q_sqrt_fit, I_squared_fit)

# Estimated parameters
a, b = params

# Generate points for the fitted line
Q_sqrt_fit_line = np.linspace(min(Q_sqrt_fit), max(Q_sqrt_fit), 100)
I_squared_fit_line = linear_function(Q_sqrt_fit_line, a, b)

# Plotting I^2 vs sqrt(Q_m) and the fitted line
plt.figure(figsize=(7, 5))
plt.scatter(np.sqrt(Q_m), I**2, label='Measured Values', color='blue', s=60)
plt.plot(Q_sqrt_fit_line, I_squared_fit_line, color='red', label='Fitted Line', linewidth=2)
plt.scatter(np.sqrt(Q_m_fit), I_squared_fit, color='green', label='Values Used for Fitting', zorder=5, s=60)
plt.xlabel('$\sqrt{Q_m}$ [kg$^{1/2}$/s$^{1/2}$]', fontsize=13)
plt.ylabel('$I^2$ [A$^2$]', fontsize=13)
# plt.title('Least Squares Fitting of $I^2$ vs $\sqrt{Q_m}$ (Using First 6 Values for Fitting)', fontsize=16)
plt.legend(fontsize=13)
plt.grid(True)

# Apply the custom formatter to the x-axis
# plt.gca().yaxis.set_major_formatter(FuncFormatter(formatter))

plt.show()

# Plotting I vs Q_m
plt.figure(figsize=(7, 5))
plt.scatter(Q_m, I, label='Measured Values', color='blue', s=60)
plt.xlabel('$Q_m$ [kg/s]', fontsize=13)
plt.ylabel('$I$ [A]', fontsize=13)
plt.legend(fontsize=13)
plt.grid(True)

plt.show()
# Output estimated parameters
print("Estimated parameters:")
print(f"a = {a}")
print(f"b = {b}")

