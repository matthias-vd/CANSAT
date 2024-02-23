import board
import busio
import time
import adafruit_bmp280

# Create I2C bus
i2c = busio.I2C(board.GP9, board.GP8)

# Create BMP280 object
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Optionally, set the BMP280's sea level pressure in hPa for more accurate altitude measurements
bmp280.sea_level_pressure = 1013.25

while True:
    print("Temperature: %0.1f C" % bmp280.temperature)
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    time.sleep(1)