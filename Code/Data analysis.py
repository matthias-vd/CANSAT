import matplotlib.pyplot as plt
import numpy as np

data = [837.711, 19.0195, 1003.15, [30.4738, 1.03703, 0.811072, 0.0, 0.813672, 0.0, 1.52953, 2.89773, 1.34175, 0.413862, 0.0, 0.0, 0.799493, 0.962432, 0.981384, 5.05734, 0.761803, 0.724051], 400, 0]
time, temperature, pressure, spectroscopy_measurements, co2, tvoc = data

# Plotting temperature and pressure over time
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(time, temperature, marker='o', color='blue')
plt.title('Temperature over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')

plt.subplot(2, 1, 2)
plt.plot(time, pressure, marker='o', color='green')
plt.title('Pressure over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (Pa)')

plt.tight_layout()
plt.show()

# Plotting spectroscopy measurements
plt.figure(figsize=(10, 5))
num_wavelengths = len(spectroscopy_measurements)
wavelengths = range(num_wavelengths)
for i in range(num_wavelengths):
    plt.plot(time, [measurement[i] for measurement in spectroscopy_measurements], label=f'Wavelength {i+1}')

plt.title('Spectroscopy Measurements over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Measurement')
plt.legend()
plt.show()

# Calculating averages
temperature_avg = np.mean(temperature)
pressure_avg = np.mean(pressure)
co2_avg = np.mean(co2)
tvoc_avg = np.mean(tvoc)

print(f"Average Temperature: {temperature_avg} °C")
print(f"Average Pressure: {pressure_avg} Pa")
print(f"Average CO2: {co2_avg}")
print(f"Average TVOC: {tvoc_avg}")
