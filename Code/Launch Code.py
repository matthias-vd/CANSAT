from board import *
from time import *
import busio
import sdcardio
import storage
import board
import time
import AS7265X_sparkfun
from AS7265X_sparkfun import AS7265X
import AS7265X_sparkfun
import adafruit_bmp280

# - Variables -
FREQ = 433.1 
NODE_ID = 120
BASESTATION_ID = 100
SLEEP = 0.5
SHELL = 1
RADIO = 1

# - Initial Setup -
# Spectroscopy
AS7265x_LED_WHITE =	0x00 #White LED is connected to x51
AS7265x_LED_IR =	0x01 #IR LED is connected to x52
AS7265x_LED_UV =	0x02 #UV LED is connected to x53
i2c = busio.I2C(board.GP17,board.GP16)
start = time.monotonic_ns()
my_as7265x = AS7265X(i2c)
my_as7265x.set_measurement_mode(AS7265X_sparkfun.MEASUREMENT_MODE_6CHAN_ONE_SHOT)
# Test Spectroscopy
my_as7265x.take_measurements()
while (not my_as7265x.data_available()):
        print("Geen data van sensor")
        while(1)        
        
# SD-card
spi = busio.SPI(GP10, MOSI=GP11, MISO=GP12)
cs = GP13
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

# RFM69
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\X08\x01\x02\x03\x04\x05\x06\x07\x08"
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, FREQ)
rfm69.node = NODE_ID

# BMP280
i2c = busio.I2C(board.GP9, board.GP8)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

#Create and open file:
with open("/sd/pico.txt", "w") as file:
    # Measurement spectrometer
    my_as7265x.take_measurements()
    all_values = my_as7265x.get_value(1)
    my_as7265x.take_measurements_with_bulb()
    all_values_bulb = my_as7265x.get_value(1)
    if SHELL == 1:
        print(all_values)
        print()
        print(all_values_bulb)
        print()
        print(bmp280.temperature)
        print()
        print(bmp280.pressure)
        print()
        print()
    if RADIO == 1:
        rfm69.send(bytes("begin","utf-8"))
        rfm69.send(bytes(all_values,"utf-8"))
        rfm69.send(bytes(",","utf-8"))
        rfm69.send(bytes(all_values_bulb,"utf-8"))
        rfm69.send(bytes(",","utf-8"))
        rfm69.send(bytes(bmp280.temperature,"utf-8"))
        rfm69.send(bytes(",","utf-8"))
        rfm69.send(bytes(bmp280.pressure,"utf-8"))
        rfm69.send(bytes(",","utf-8"))
        rfm69.send(bytes("end","utf-8"))
        
    sleep(SLEEP)