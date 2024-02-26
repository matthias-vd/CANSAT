import board
import busio
import digitalio
import adafruit_bno055
import sdcardio
import storage
import adafruit_rfm69
import time
from adafruit_bme280 import basic as adafruit_bmp280
from pwmio import PWMOut 
from music import play_tune
import math

################# hoogteberekening ############"


local_altitude = 630
local_pressure = 943
    
#######################

# Define radio parameters.
RADIO_FREQ_MHZ = 433.3  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.
    
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node
BASESTATION_ID = 100 # ID of the node (base station) to be contacted


################## RFM 69 ############################


# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)
        # Define the onboard LED
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

try:
           # Initialize SPI bus.
    spi = busio.SPI(board.GP18, board.GP19, board.GP16)
                # Initialze RFM radio
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)


    rfm69.encryption_key = ( ENCRYPTION_KEY )
    rfm69.node    = NODE_ID # This instance is the node 120

    print( 'Freq            :', rfm69.frequency_mhz )
    print( 'NODE            :', rfm69.node )
    
except:
    
    print("!! RFM69 !! error")

################ BMP 280 ##########################

try:
    i2c = busio.I2C(board.GP9,board.GP8)   # uses board.SCL and board.SDA
    bme280 = adafruit_bmp280.Adafruit_BME280_I2C(i2c)
except:
    pass


############### BNO 055 ########################

try:
    sensor = adafruit_bno055.BNO055_I2C(i2c)
except:
    pass

last_val = 0xFFFF

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

############# SD CARD #################################

try:
    spi = busio.SPI(board.GP14, MOSI=board.GP15, MISO=board.GP12)
    cs = board.GP13
    sd = sdcardio.SDCard(spi, cs)

    vfs = storage.VfsFat(sd)
    storage.mount(vfs, '/sd')
except:
    pass

############## BUZZER ##############################"

 # set up buzzer with variable frequency
try:
    buzzer = PWMOut(board.GP11, variable_frequency = True)
except:
    pass

############### VERZENDEN PAKKET #####################

tune = ['E5:0.2','D8:0.2'] 
counter = 1
rfm69.ack_retries = 3 # 3 attempt to receive ACK
rfm69.ack_wait    = 0.5 # 500ms, time to wait for ACK 
rfm69.destination = BASESTATION_ID # Send to specific node 100
#hoogte = 60
start_time = time.monotonic()
max_hoogte = local_altitude

while True:
    
    seconds = time.monotonic()
    #print(seconds)
    
    try:
        print("Temperature: {} degrees C".format(sensor.temperature))
        print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
        print("Magnetometer (microteslas): {}".format(sensor.magnetic))
        print("Gyroscope (rad/sec): {}".format(sensor.gyro))
        print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
        print("Gravity (m/s^2): {}".format(sensor.gravity))
        print(" ")
    except:
        print("!! BNO055 !!")
        
    try:
        print("Temperature: %0.1f C" % bme280.temperature)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        
        alt = local_altitude + (287.06*bme280.temperature/9.80665) * math.log(bme280.pressure/local_pressure)
        if(alt > max_hoogte):
            max_hoogte = alt
        print(alt)
        
        
    except:
        print("!! BMP280 Error !!")
        
    print("Send message %i!" % counter)
    
    try:
    
        msg_sd = "%i, %5.2f, %5.2f, %s, %s, %s, %s, %s, %s;" % (seconds,bme280.temperature,bme280.pressure,str(sensor.temperature),str(sensor.acceleration),str(sensor.magnetic),str(sensor.gyro),str(sensor.linear_acceleration),str(sensor.gravity))
        msg_rfm = "%i, %5.2f, %5.2f;" % (seconds,bme280.temperature,bme280.pressure)
    
    except:
        
        msg_sd("FAIL")
        msg_rfm("FAIL")
    
    try:
        rfm69.send(bytes(msg_rfm,"utf-8") )
    except:
        pass
    
    with open("/sd/pico.txt", "a") as file:
        file.write(msg_sd)
        file.write("\n")
        
    if(max_hoogte > 750):
        if(alt < 50):
            play_tune(buzzer, tune) 
    
    counter += 1
    time.sleep(5)



