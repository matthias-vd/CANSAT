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
import adafruit_sgp30
import digitalio


def init_i2c():
    return busio.I2C(board.GP9, board.GP8,frequency=100000)

def init_spi_sd():
    return busio.SPI(GP14, MOSI=GP15, MISO=GP12)

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
        rfm69.tx_power = 20
        #rfm69.encryption_key = "SPECSATVLOT2024"
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
    
def init_sgp30(i2c):
    try:
        sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        print("SGP30 INITIALISED")
        return sgp30
    except ValueError:
        print("ERROR: SGP30 not connected")
        return None
