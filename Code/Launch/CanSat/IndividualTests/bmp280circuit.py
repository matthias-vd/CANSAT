import board
import busio
import time
import adafruit_bmp280

# Create I2C bus
i2c = busio.I2C(board.GP9, board.GP8)               # Dit werkt voor connectie met Qwicc, pas pins aan indien nodig.

# Create BMP280 object
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

while True:
    print("Temperature: %0.1f C" % bmp280.temperature)     # Geef temperatuur in °C
    print("Pressure: %0.1f hPa" % bmp280.pressure)         # Geef druk in hPa
    time.sleep(1)