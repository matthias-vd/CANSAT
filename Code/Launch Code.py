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
import adafruit_rfm69
import digitalio

# - Variables -
FREQ = 433.0
NODE_ID = 120
BASESTATION_ID = 100
SLEEP = 0.5
SHELL = 1
RADIO = 1
SDCARD = 1

# - Initial Setup -
# Spectroscopy
AS7265x_LED_WHITE =	0x00 #White LED is connected to x51
AS7265x_LED_IR =	0x01 #IR LED is connected to x52
AS7265x_LED_UV =	0x02 #UV LED is connected to x53
i2c= busio.I2C(board.GP17,board.GP16)
start = time.monotonic()
my_as7265x = AS7265X(i2c)
my_as7265x.set_measurement_mode(AS7265X_sparkfun.MEASUREMENT_MODE_6CHAN_ONE_SHOT)
# Test Spectroscopy
#my_as7265x.take_measurements()
#while (not my_as7265x.data_available()):
#        print("Geen data van sensor")    
            
# SD-card
try: 
    SPI_SD = busio.SPI(GP10, MOSI=GP11, MISO=GP12)
    CS_SD = GP13
    sd = sdcardio.SDCard(SPI_SD, CS_SD)
    vfs = storage.VfsFat(sd)
    storage.mount(vfs, '/sd')
except OSError:
    print("SD not connected")
    SDCARD = 0
    

# RFM69
SPI_RFM = busio.SPI(board.GP6, board.GP7, board.GP4)
CS_RFM = digitalio.DigitalInOut(board.GP5)
RESET_RFM = digitalio.DigitalInOut(board.GP3)
LED_RFM = digitalio.DigitalInOut(board.LED)
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\X08\x01\x02\x03\x04\x05\x06\x07\x08"
try: 
    rfm69 = adafruit_rfm69.RFM69(SPI_RFM, CS_RFM, RESET_RFM, FREQ)
    rfm69.node = NODE_ID
except RuntimeError:
    RADIO = 0
    print("RFM not connected")
    
rfm69.ack_retries = 3 # 3 attempt to receive ACK
rfm69.ack_wait    = 0.5 # 500ms, time to wait for ACK 
rfm69.destination = BASESTATION_ID # Send to specific node 100


# BMP280
#i2c_bmp280 = busio.I2C(board.GP24, board.GP25)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

#Create and open file:
#with open("/sd/pico.txt", "w") as file:
while True:
    # Measurement spectrometer
    my_as7265x.take_measurements()
    all_values = my_as7265x.get_value(1)
    my_as7265x.take_measurements_with_bulb()
    all_values_bulb = my_as7265x.get_value(1)
    
    seconds = time.monotonic()
    msg_rfm = "%i, %5.2f, %5.2f;" % (seconds,bmp280.temperature,bmp280.pressure)
    
    
    if SHELL == 1:
        print(msg_rfm)
        print()
    if RADIO == 1:
        rfm69.send(bytes("test","utf-8"))
        #ack = rfm69.send(msg_rfm)
        #print(ack)
        #print(msg_rfm)
    #if SDCARD = 1:
        
    sleep(SLEEP)