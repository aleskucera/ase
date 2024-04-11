import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exp_func(t, a, b):
    return a * np.exp(b / (t + 273.15))


def linear_func(t, a, b):
    return a * t + b


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
    # order = np.argsort(pt100)
    order = np.arange(len(pt100))
    pt100 = pt100[order]
    ntc1 = ntc1[order]
    ntc2 = ntc2[order]
    egr_sens = egr_sens[order]

    # Curve fitting for NTC1
    popt_ntc1, pcov_ntc1 = curve_fit(exp_func, pt100, ntc1, bounds=(0, np.inf))

    # Curve fitting for NTC2
    popt_ntc2, pcov_ntc2 = curve_fit(exp_func, pt100, ntc2, bounds=(0, np.inf))

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


if __name__ == '__main__':
    main()
