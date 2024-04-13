import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import least_squares


def exp_func(t, a, b):
    return a * np.exp(b / (t + 273.15))


def linear_func(t, a, b):
    return a * t + b


def ideal_characteristic(t):
    """ Linear function that intersects two points
    p1: (-40, 4.5)
    p2: (125, 0.5)

    y = a * x + b

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    """

    a = (0.5 - 4.5) / (125 + 40)
    b = 4.5 + a * 40
    return a * t + b

def voltage_divider(t, r1, r2):
    """ Linearization circuit for NTC.

    Vout = Vin * (R2 + R_ntc(t)) / (R1 + R2 + R_ntc(t))

    Args:
        t: temperature in °C
        r1: resistance of R1 in Ohm
        r2: resistance of R2 in Ohm

    Returns:
        Vout: output voltage of the voltage divider in V for the Vin = 1 V
    """

    r_ntc = exp_func(t, 0.02, 3512.81)
    r2_ntc = (r2 * r_ntc) / (r2 + r_ntc)
    return 5 * r2_ntc / (r1 + r2_ntc)

# def residuals(params):
#     r1, r2 = params
#     t = np.linspace(-40, 125, 100)
#     ntc_lin = voltage_divider(t, r1, r2, 0.02, 3512.81)
#     ideal_lin = ideal_characteristic(t)
#     return ntc_lin - ideal_lin

def main():
    temp = np.array([-20, 0, 20, 40, 60, 80, 100])
    ll_ntc = np.array([10000, 4000, 1800, 800, 400, 200, 100])
    hl_ntc = np.array([20000, 7000, 3000, 1300, 700, 400, 220])

    data = np.load('measurements.npz')
    meas_time = data['meas_time']
    ntc1 = data['ntc1']
    ntc2 = data['ntc2']
    egr_sens = data['egr_sens']
    pt100 = data['pt100']

    # Sort by temperature
    order = np.argsort(pt100)
    # order = np.arange(len(pt100))
    pt100 = pt100[order]
    ntc1 = ntc1[order]
    ntc2 = ntc2[order]
    egr_sens = egr_sens[order]

    # Curve fitting for NTC1
    popt_ntc1, pcov_ntc1 = curve_fit(exp_func, pt100, ntc1, bounds=(0, np.inf))
    print(f"NTC1 curve fitting parameters: a = {popt_ntc1[0]:.2f}, b = {popt_ntc1[1]:.2f}")

    # Curve fitting for NTC2
    popt_ntc2, pcov_ntc2 = curve_fit(exp_func, pt100, ntc2, bounds=(0, np.inf))
    print(f"NTC2 curve fitting parameters: a = {popt_ntc2[0]:.2f}, b = {popt_ntc2[1]:.2f}")

    # Plotting NTC1 vs Temperature with Low and High Limits
    plt.figure(figsize=(6, 4))
    plt.plot(pt100, ntc1, marker='o', color='blue', linewidth=1, markeredgewidth=1, markersize=2)
    plt.plot(temp[2:], ll_ntc[2:], marker='o', color='green', linewidth=2)
    plt.plot(temp[2:], hl_ntc[2:], marker='s', color='red', linewidth=2)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('NTC1 [Ohm]', fontsize=11)
    # plt.title('NTC1 Resistance vs Temperature', fontsize=16)
    plt.legend(['NTC1', 'Low Limit', 'High Limit'])
    plt.grid(True)
    plt.show()

    # Plotting NTC2 vs Temperature with Low and High Limits
    plt.figure(figsize=(6, 4))
    plt.plot(pt100, ntc2, marker='o', color='blue', linewidth=1, markeredgewidth=1, markersize=2)
    plt.plot(temp[2:], ll_ntc[2:], marker='o', color='green', linewidth=2)
    plt.plot(temp[2:], hl_ntc[2:], marker='s', color='red', linewidth=2)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('NTC2 [Ohm]', fontsize=11)
    # plt.title('NTC2 Resistance vs Temperature', fontsize=16)
    plt.legend(['NTC2', 'Low Limit', 'High Limit'])
    plt.grid(True)
    plt.show()

    # Plotting NTC1 vs Temperature with extrapolated curve
    plt.figure(figsize=(6, 4))
    plt.plot(pt100, ntc1, marker='o', color='orange', linewidth=1, markeredgewidth=1, markersize=3)
    plt.plot(pt100, exp_func(pt100, *popt_ntc1), color='blue', linestyle='--', linewidth=3)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('NTC1 [Ohm]', fontsize=11)
    # plt.title('NTC1 Resistance vs Temperature with Extrapolated Curve', fontsize=16)
    plt.legend(['NTC1', 'Extrapolated Curve'])
    plt.grid(True)
    plt.show()

    # Plotting NTC2 vs Temperature with extrapolated curve
    plt.figure(figsize=(6, 4))
    plt.plot(pt100, ntc2, marker='o', color='orange', linewidth=1, markeredgewidth=1, markersize=3)
    plt.plot(pt100, exp_func(pt100, *popt_ntc2), color='blue', linestyle='--', linewidth=3)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('NTC2 [Ohm]', fontsize=11)
    # plt.title('NTC2 Resistance vs Temperature with Extrapolated Curve', fontsize=12)
    plt.legend(['NTC2', 'Extrapolated Curve'])
    plt.grid(True)
    plt.show()

    # Plot the EGR sensor vs Temperature
    plt.figure(figsize=(6, 4))
    plt.plot(pt100[1:], egr_sens[1:], marker='o', color='blue', linewidth=1, markeredgewidth=1, markersize=2)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('EGR Sensor [V]', fontsize=11)
    # plt.title('EGR Sensor Voltage vs Temperature', fontsize=16)
    plt.grid(True)
    plt.show()

    # Interpolate the EGR data that are larger than 50 with the linear function
    egr = egr_sens[egr_sens > 50]
    temp_egr = pt100[egr_sens > 50]
    popt_egr, pcov_egr = curve_fit(linear_func, temp_egr, egr)

    # Plot the EGR sensor vs Temperature with extrapolated curve
    plt.figure(figsize=(6, 4))
    plt.plot(pt100[1:], egr_sens[1:], marker='o', color='orange', linewidth=1, markeredgewidth=1, markersize=3)
    plt.plot(pt100[1:], linear_func(pt100[1:], *popt_egr), color='blue', linestyle='--', linewidth=3)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('EGR Sensor [Ohm]', fontsize=11)
    # plt.title('EGR Sensor Voltage vs Temperature with Extrapolated Curve', fontsize=16)
    plt.legend(['EGR Sensor', 'Extrapolated Curve'])
    plt.grid(True)
    plt.show()

    # Print the linear function parameters
    print('EGR Sensor Linear Function Parameters: a =', popt_egr[0], 'b =', popt_egr[1])

    # Plot the NTC1 and NTC2 curves with the ideal characteristic
    t = np.linspace(-40, 125, 100)
    ideal_lin = ideal_characteristic(t)

    # Apply curve fitting for NTC
    popt_r, pcov_r = curve_fit(voltage_divider, t, ideal_lin, bounds=(0, np.inf))
    print(f"NTC curve fitting parameters: R1 = {popt_r[0]:.2f}, R2 = {popt_r[1]:.2f}")

    plt.figure(figsize=(6, 4))
    plt.plot(t, voltage_divider(t, *popt_r), color='blue', linewidth=2)
    plt.plot(t, ideal_lin, color='green', linewidth=2)
    plt.xlabel('Temperature [°C]', fontsize=11)
    plt.ylabel('Voltage [V]', fontsize=11)
    # plt.title('NTC1, NTC2 and Ideal Characteristic', fontsize=16)
    plt.legend(['Linearized NTC1', 'Ideal Characteristics'])
    plt.grid(True)

    plt.show()




if __name__ == '__main__':
    main()
