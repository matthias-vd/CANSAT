from machine import I2C
# BME280 aslo work for BMP280
from bme280 import BME280, BMP280_I2CADDR
from time import sleep
i2c = I2C(1)		#SDA met GP14 en SCL met GP15; IC2 bus 0 wil niet werken.
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )

while True:
    # returns a tuple with (temperature, pressure_hPa, humidity)
    print( bmp.raw_values )
    sleep(1)