import init
import helper
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

#### INITS

FREQ = 433
NODE_ID = 120
BASESTATION_ID = 100
SHELL = 1
SLEEP = 2
p0 = 101325  # Pressure at sea level in Pa
T0 = 288.15  # Standard temperature at sea level in K
h0 = 5

#### COMMUNICATION BUSSES

i2c = init.init_i2c()
spi_sd = init.init_spi_sd()
spi_rfm = init.init_spi_rfm()

##### SENSOR INIT

sd = init.init_sd(spi_sd)
rfm = init.init_rfm69(spi_rfm,FREQ,NODE_ID,BASESTATION_ID)
bmp = init.init_bmp280(i2c)
spec = init.init_as7265x(i2c)

#### LETSGOO

start = time.monotonic()
h = h0
max_h = 0

while True:
    
    begin_loop = time.monotonic()
    seconds = begin_loop-start
    measurements = [seconds]
    bmp_values = 0
    
    #MEASURE AND CALCULATE
    helper.bmp_measurement(bmp,bmp_values,measurements)
    helper.spectral_measurement(spec,measurements)
    h = helper.calculate_height(bmp,p0,T0,h0,h,max_h)

    # COMMUNICATION
    helper.send_package(rfm,bmp_values,measurements)
    
    # SAVING/PRINTING VALUES
    helper.save_measurements_sd(sd,measurements)
    helper.save_measurements_local(measurements)
    helper.print_shell(SHELL,measurements)
    
    # BUZZER
    helper.start_buzzer(h,max_h)          
        
    end_loop = time.monotonic()
    delta_time = end_loop-begin_loop
    #print(delta_time) UITVOERING LOOP DUURT GEMIDDELD 1,65s! DATA WORDT DUS NIET 1 MAAL PER SECONDE NAAR GROUND GESTUURD.
        
    time.sleep(SLEEP-(delta_time))