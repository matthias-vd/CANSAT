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

# GENERAL Variables -
FREQ = 433.0
NODE_ID = 120
BASESTATION_ID = 100
SLEEP = 2
SHELL = 1
RADIO = 1
SDCARD = 1
SPECSENSOR = 1
BMP = 1


# INIT I2C 
i2c= busio.I2C(board.GP17,board.GP16)
# INIT SPI FOR SD & RFM
SPI_SD = busio.SPI(board.GP10, board.GP11, board.GP12)
CS_SD = board.GP13
SPI_RFM = busio.SPI(board.GP6, board.GP7, board.GP4)
CS_RFM = digitalio.DigitalInOut(board.GP5)

# - Initial Setup -

# Spectroscopy

AS7265x_LED_WHITE =	0x00 #White LED is connected to x51
AS7265x_LED_IR =	0x01 #IR LED is connected to x52
AS7265x_LED_UV =	0x02 #UV LED is connected to x53

try:
    my_as7265x = AS7265X(i2c)
    my_as7265x.set_measurement_mode(AS7265X_sparkfun.MEASUREMENT_MODE_6CHAN_ONE_SHOT)
except ValueError:
    print("AS7265x not connected")
    SPECSENSOR = 0
 
# SD-card
try:    
    sd = sdcardio.SDCard(SPI_SD, CS_SD)
    vfs = storage.VfsFat(sd)
    storage.mount(vfs, '/sd')
except OSError as e:
    print("SD not connected",e)
    SDCARD = 0
    
# RFM69
RESET_RFM = digitalio.DigitalInOut(board.GP3)
LED_RFM = digitalio.DigitalInOut(board.LED)
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\X08\x01\x02\x03\x04\x05\x06\x07\x08"

try: 
    rfm69 = adafruit_rfm69.RFM69(SPI_RFM, CS_RFM, RESET_RFM, FREQ)
    rfm69.node = NODE_ID
except RuntimeError:
    RADIO = 0
    print("RFM not connected")
    
#rfm69.ack_retries = 3 # 3 attempt to receive ACK
#rfm69.ack_wait    = 0.5 # 500ms, time to wait for ACK 
#rfm69.destination = BASESTATION_ID # Send to specific node 100

# BMP280
try:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
except ValueError:
    print("BMP not connected")
    BMP = 0
    
  
    
#### LETSGOO

start = time.monotonic()

while True:
    
    begin_loop = time.monotonic()
    seconds = begin_loop-start
    measurements = [seconds]
    
    # Measurement spectrometer
    if SPECSENSOR == 1:
        my_as7265x.take_measurements()
        all_values = my_as7265x.get_value(1)
        my_as7265x.take_measurements_with_bulb()
        all_values_bulb = my_as7265x.get_value(1)
        measurements.append(all_values_bulb)  
        
    if BMP == 1:
        bmp_values = [bmp280.temperature,bmp280.pressure]
        measurements.append(bmp_values)
        # ADD HEIGHTCALCULATIONS HERE
      
    if SHELL == 1:
        print(measurements)

    if(RADIO == 1 and BMP == 1):
        rfm69.send(bytes("test","utf-8"))
        rfm69.send(bytes(str(bmp_values),"utf-8"))
        #ack = rfm69.send(measurements)
        
    if SDCARD == 1:
        with open("/sd/measurements.txt", "a") as file:
            file.write(measurements)
    
    #with open("/measurements.txt", "a") as f:
    #    f.write(str(all_values_bulb) + '\n')
        
    end_loop = time.monotonic()
    delta_time = end_loop-begin_loop
    #print(delta_time) UITVOERING LOOP DUURT GEMIDDELD 1,65s! DATA WORDT DUS NIET 1 MAAL PER SECONDE NAAR GROUND GESTUURD.
        
    sleep(SLEEP-(delta_time))