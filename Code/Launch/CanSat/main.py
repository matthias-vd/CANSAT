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
import adafruit_sgp30
import digitalio
import sys
from pwmio import PWMOut 
#from buzzer import play_tune

#### INITS
FREQ = 434.9
NODE_ID = 120
BASESTATION_ID = 100
SHELL = 1
SLEEP = 2
p0 = 101900  # Pressure at sea level in Pa
T0 = 273.15  # Standard temperature at sea level in K
h0 = 630 # beginhoogte
counter = 0
#buzzer_pin = board.GP26

#### COMMUNICATION BUSSES

i2c = init.init_i2c()
spi_sd = init.init_spi_sd()
spi_rfm = init.init_spi_rfm()

##### SENSOR INIT
#buzzer = init.init_buzzer(buzzer_pin)
sd = init.init_sd(spi_sd)
bmp = init.init_bmp280(i2c)
spec = init.init_as7265x(i2c)
sgp = init.init_sgp30(i2c)
rfm = init.init_rfm69(spi_rfm,FREQ,NODE_ID,BASESTATION_ID)

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
        try:
            bmp_values = helper.bmp_measurement(bmp,measurements)
        except OSError:
            print("ERROR: Connectie BMP verloren mid-flight")
        #SPECTRAL MEASUREMENT
        try:
            helper.spectral_measurement(spec,measurements)
        except OSError:
            print("ERROR: Connectie spectroscopiesensor verloren mid-flight")
        #HEIGTH MEASUREMENT    
        try:
            h = helper.calculate_height(bmp,p0,T0,h0,h,max_h)
        except OSError:
            print("ERROR: Connectie BMP verloren mid-flight")
        except AttributeError:
            print("ERROR: BMP levert geen temperatuurwaarden")
        counter = counter + 1
        
        # COMMUNICATION
        try:
            helper.send_package(rfm,bmp_values,measurements)
        except TimeoutError:
            print("ERROR: RFM69 fout bekabeled!")
        
        #####SGP30#####"
        
        try:
            helper.co2_measurement(sgp,measurements)
        except OSError:
            print("ERROR: Connectie CO2-sensor verloren")
            
        
        # BUZZER
        #if(max_h+h0 > 500 and h-h0 < 100):
        #helper.start_buzzer(buzzer,400,1)
            
        helper.save_measurements_local(measurements)
        helper.print_shell(SHELL,measurements)
        #helper.print_shell(SHELL,bmp_values)
        
        end_loop = time.monotonic()
        delta_time = end_loop-begin_loop
         # SAVING/PRINTING VALUES
        try:
            helper.save_measurements_sd(sd,measurements)
        except OSError:
            print("ERROR: Connectie SD-kaart verloren")
            """try:
                print("SD-kaart proberen herinitialiseren")
                spi_sd = init.init_spi_sd()
                sd = init.init_sd(spi_sd)
                sd = sdcardio.SDCard(spi_sd, board.GP9)
                vfs = storage.VfsFat(sd)
                storage.mount(vfs, '/sd')
            except Exception as error:
                print("SD-kaart herinitialisatie mislukt!", error)"""
        try:    
            time.sleep(SLEEP-(delta_time))
        except:
            print("ERROR: Delta tijd kleiner!")
    except KeyboardInterrupt:
        print("Manuele interrupt")
        sys.exit()
