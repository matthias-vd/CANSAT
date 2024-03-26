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
import sys

#### INITS
FREQ = 433.2
NODE_ID = 120
BASESTATION_ID = 100
SHELL = 1
SLEEP = 2
p0 = 101325  # Pressure at sea level in Pa
T0 = 293.15  # Standard temperature at sea level in K
h0 = 10 # beginhoogte


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
    try:
        begin_loop = time.monotonic()
        seconds = begin_loop-start
        measurements = [seconds]
        bmp_values = []
        
        #MEASURE AND CALCULATE
        bmp_values = helper.bmp_measurement(bmp,measurements)
        helper.spectral_measurement(spec,measurements)
        h = helper.calculate_height(bmp,p0,T0,h0,h,max_h)

        # COMMUNICATION
        helper.send_package(rfm,bmp_values,measurements)
        
        # SAVING/PRINTING VALUES
        helper.save_measurements_sd(sd,measurements)
        helper.save_measurements_local(measurements)
        #helper.print_shell(SHELL,measurements)
        #helper.print_shell(SHELL,bmp_values)
        
        # BUZZER
        helper.start_buzzer(h,max_h)          
            
        end_loop = time.monotonic()
        delta_time = end_loop-begin_loop
        #print(delta_time) #UITVOERING LOOP DUURT GEMIDDELD 1,65s! DATA WORDT DUS NIET 1 MAAL PER SECONDE NAAR GROUND GESTUURD.
        try:    
            time.sleep(SLEEP-(delta_time))
        except:
            print("ERROR: Delta tijd kleiner!")
    except KeyboardInterrupt:
        print("Manuele interrupt")
        sys.exit()