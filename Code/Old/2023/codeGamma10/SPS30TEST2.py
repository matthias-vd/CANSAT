from machine import I2C,Pin
import time
from spsHELPER import *
#from SPSTESTTHIJS import *
import struct

######### INIT i2C communicatie en zoek of apparaat is aangelsloten ##################

i2c = I2C(1,sda=Pin(14),scl=Pin(15),freq=100000) # FREQUENTIE INSTELLEN op 100kHz IS CRUCIAAL?
time.sleep(1)
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C device found")
elif len(devices) > 1:
    print("Multiple I2C devices found -")
    for d in devices:
        print("  0x{:02X}".format(d))
else:
    print("I2C device found at 0x{:02X}".format(devices[0]))
    device = devices[0]    
    SPS30_ADR = device
    pm_sensor = SPS30()    


############### NEW TEST ##################

pm_sensor = SPS30()

#################### NORMAL

START_MEAS   = [0x00, 0x10]
STOP_MEAS    = [0x01, 0x04]
R_DATA_RDY   = [0x02, 0x02]
R_VALUES     = [0x03, 0x00]
RW_AUTO_CLN  = [0x80, 0x04]
START_CLN    = [0x56, 0x07]
R_ARTICLE_CD = [0xD0, 0x25]
R_SERIAL_NUM = [0xD0, 0x33]
RESET        = [0xD3, 0x04]

# Start measurement

pm_sensor.start_measurement() # dit werkt
time.sleep(1)

teller = 13

#Read measurement data
while teller < 15:
    print(str(teller))
    #https://github.com/feyzikesim/sps30/tree/master/sps30
    #i2c.writeto(SPS30_ADR,bytearray(R_VALUES))
    #data = pm_sensor.read_measured_values_new()
    #data = i2c.readfrom(SPS30_ADR,60)  # 60 is het aantal verwachtte bytes
    
    if pm_sensor.read_measured_values_new() == pm_sensor.MEASURED_VALUES_ERROR:
        raise Exception("MEASURED VALUES CRC ERROR!")
    else:
        print ("PM2.5 Value in µg/m3: " + str(pm_sensor.dict_values['pm2p5']))
        print ("PM10.0 Value in µg/m3: " + str(pm_sensor.dict_values['pm10p0']))

    teller +=1
    time.sleep(1)
    
pm_sensor.stop_measurement() # dit werkt

