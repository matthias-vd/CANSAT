from machine import Pin, I2C
import struct
from time import sleep
import ubinascii

def calculateCRC(input):
    crc = 0xFF
    for i in range (0, 2):
        crc = crc ^ input[i]
        for j in range(8, 0, -1):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
    crc = crc & 0x0000FF
    return crc

def checkCRC(result):
    for i in range(2, len(result), 3):
        data = []
        data.append(result[i-2])
        data.append(result[i-1])

        crc = result[i]

        if crc == calculateCRC(data):
            crc_result = True
        else:
            crc_result = False
    return crc_result

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

##convert a 4-byte hex string to a floating-point value in big-endian byte order.

def hex_to_bytes(hex_string):
    bytes_array = bytearray()
    for i in range(0, len(hex_string), 2):
        byte = int(hex_string[i:i+2], 16)
        bytes_array.append(byte)
    return bytes_array

def convertPMValues(value):
    string_value = '{:08x}'.format(value)
    byte_value = hex_to_bytes(string_value)
    return struct.unpack('>f', byte_value)[0]

class SPS30():
    SPS_ADDR = 0x69

    START_MEAS   = [0x00, 0x10]
    STOP_MEAS    = [0x01, 0x04]
    R_DATA_RDY   = [0x02, 0x02]
    R_VALUES     = [0x03, 0x00]
    RW_AUTO_CLN  = [0x80, 0x04]
    START_CLN    = [0x56, 0x07]
    R_ARTICLE_CD = [0xD0, 0x25]
    R_SERIAL_NUM = [0xD0, 0x33]
    RESET        = [0xD3, 0x04]

    NO_ERROR = 1
    ARTICLE_CODE_ERROR = -1
    SERIAL_NUMBER_ERROR = -2
    AUTO_CLN_INTERVAL_ERROR = -3
    DATA_READY_FLAG_ERROR = -4
    MEASURED_VALUES_ERROR = -5

    dict_values = {"pm1p0"  : None,
                   "pm2p5"  : None,
                   "pm4p0"  : None,
                   "pm10p0" : None,
                   "nc0p5"  : None,
                   "nc1p0"  : None,
                   "nc2p5"  : None,
                   "nc4p0"  : None,
                   "nc10p0" : None,
                   "typical": None}

    def __init__(self, i2c_bus=1, scl_pin=15, sda_pin=14):
        self.bus = I2C(i2c_bus, scl=Pin(scl_pin), sda=Pin(sda_pin),freq=100000)
        
    def start_measurement(self):
        self.START_MEAS.append(0x03)
        self.START_MEAS.append(0x00)

        crc = calculateCRC(self.START_MEAS[2:4])
        self.START_MEAS.append(crc)

        self.bus.writeto(self.SPS_ADDR,bytearray(self.START_MEAS))
        
    def stop_measurement(self):
        self.bus.writeto(self.SPS_ADDR,bytearray(self.STOP_MEAS))
       
    def read_measured_values_new(self):
        
        result = []
        read = bytes(60)
        #read = bytearray(48)

        self.bus.writeto(self.SPS_ADDR,bytearray(self.R_VALUES))
        read = self.bus.readfrom(self.SPS_ADDR,60)
        
        print(read)
        
        for i in range(len(read)):
            result.append(read[i])
 
             
        if checkCRC(result):
            self.parse_sensor_values(result)
            return self.NO_ERROR

        else:
            return self.MEASURED_VALUES_ERROR 
        
    def parse_sensor_values(self, input):
        index = 0
        pm_list = []        
       
        for i in range (4, len(input), 6):
            value = input[i] + input[i-1] * pow(2, 8) +input[i-3] * pow(2, 16) + input[i-4] * pow(2, 24)
            pm_list.append(value)
            

        for i in self.dict_values.keys():
            self.dict_values[i] = convertPMValues(pm_list[index])
            index += 1
            
        #print(dict_values)
            
    def read_article_code(self):
        result = []
        article_code = []

        self.bus.writeto(self.SPS_ADDR,bytearray(self.R_ARTICLE_CD))
        result = self.bus.readfrom(self.SPS_ADDR, 48)

        print(result)
        
        if checkCRC(result):
            for i in range (2, len(result), 3):
                article_code.append(chr(result[i-2]))
                article_code.append(chr(result[i-1]))
                #print(str("".join(article_code)))
            return str("".join(article_code))
        else:
            return self.ARTICLE_CODE_ERROR
        

            