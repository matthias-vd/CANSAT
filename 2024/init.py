from board import *
from time import *
import busio
import sdcardio
import storage
import board
import time
import AS7265X_sparkfun
from AS7265X_sparkfun import AS7265X
import adafruit_bmp280
import adafruit_rfm69
import digitalio

def init_i2c():
    return busio.I2C(board.GP17, board.GP16)

def init_spi_sd():
    return busio.SPI(board.GP10, board.GP11, board.GP12)

def init_spi_rfm():
    return busio.SPI(board.GP6, board.GP7, board.GP4)

def init_sd(spi_sd):
    try:
        sd = sdcardio.SDCard(spi_sd, board.GP13)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, '/sd')
        print("SD INITIALISED")
        return sd
    except OSError as e:
        print("SD not connected", e)
        return None

def init_rfm69(spi_rfm,freq,node_id,basestation_id):
    RESET_RFM = digitalio.DigitalInOut(board.GP3)
    CS_RFM = digitalio.DigitalInOut(board.GP5)

    try:
        rfm69 = adafruit_rfm69.RFM69(spi_rfm, CS_RFM, RESET_RFM, freq)
        rfm69.node = node_id
        print("RFM INITIALISED")
        return rfm69
    except RuntimeError:
        print("RFM not connected")
        return None

def init_bmp280(i2c):
    try:
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        print("BMP INITIALISED")
        return bmp280
    except ValueError:
        print("BMP not connected")
        return None

# Spectroscopy
def init_as7265x(i2c):
    try:        
        my_as7265x = AS7265X(i2c)
        my_as7265x.set_measurement_mode(AS7265X_sparkfun.MEASUREMENT_MODE_6CHAN_ONE_SHOT)
        print("AS7265x INITIALISED")
        return my_as7265x
    except ValueError:
        print("AS7265x not connected")
        return None