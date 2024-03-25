from machine import I2C,Pin
import time
from sys import exit

######### INIT i2C communicatie en zoek of apparaat is aangelsloten ##################

i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=100000) # FREQUENTIE INSTELLEN op 400kHz IS CRUCIAAL???
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
    GDK101_ADDR = device
    #pm_sensor = SPS30()    

#exit()
############### NEW TEST ##################

#pm_sensor = SPS30()

#################### NORMAL

##### COMMANDOS ######
    
RESET = 0xA0
STATUS = 0xB0
TIME = 0xB1
MEAS10 = 0xB2
MEAS1 = 0xB3
FIRM = 0xB4

CMD_REG_ADDR = 0x00  # Address of the command register
MEAS_REG_ADDR = 0x01  # Address of the measurement register
FIRMWARE_CMD = 0x19  # Command to read the firmware version

# Function to read the gamma radiation data from the sensor
def read_gamma():
    # Send the command to the sensor
    i2c.writeto(GDK101_ADDR, bytearray(MEAS1))
    # Wait for the sensor to respond
    time.sleep(0.1)    
    data = bytes(2)
    # Read the response from the sensor
    data = i2c.readfrom(GDK101_ADDR, 2)
    print(data)
    # Extract the gamma radiation value from the response
    gamma = (data[2] << 8) + data[3]
    return gamma

def read_firmware_version():
    
    i2c.writeto(GDK101_ADDR, bytearray(FIRM))
    time.sleep(0.1)
    data = bytearray(2)
    data = i2c.readfrom(GDK101_ADDR, 2)
    firmware_version = (data[2] << 8) + data[3]
    return firmware_version


def read_firmware():
    # Send the firmware version command to the sensor
    i2c.writeto(GDK101_ADDR, bytearray(firm))
    # Wait for the sensor to respond
    time.sleep(1)
    # Read the response from the sensor
    response = i2c.readfrom(GDK101_ADDR, 2)
    # Extract the firmware version from the response
    firmware = response[1]
    return firmware

# Main loop to read and print the gamma radiation value
while True:
    firm = read_firmware()
    print("firware:", firm)
    gamma = read_gamma()
    print("Gamma radiation:", gamma)
    time.sleep(1)