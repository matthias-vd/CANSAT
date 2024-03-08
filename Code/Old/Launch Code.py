# - Bekabeling -
"""
WIRING
"""
# - Libraries -
# "Basic" libaries
from machine import SPI, I2C, Pin, ADC
# Radiocommunicatiemodule
from rfm69 import RFM69
# Druksensor/weersensor
from bme280 import BME280, BMP280_I2CADDR
# Tijd
import time

# - Variables -
SHELL = 1 # Logging
FREQ = 433.1 # Frequentie
IDENTIFICATIE = "SPECSAT" # Unieke identificatie - enkel ter controle!
NODE_ID        = 120 
BASESTATION_ID = 100
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08" # Dataversleuteling
SLEEP = 0.5 # Tijd tussen dataverwerking en -verzending


# - Initiële Setup -
# Radiocommunicatiemodule
rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz  = FREQ
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node           = NODE_ID 
rfm.destination    = BASESTATION_ID
# Druksensor
bmp = BME280(i2c=i2c, address=BMP280_I2CADDR)
# Temperatuursensor
adc = ADC(Pin(26))


while True:
    # Temperatuurdata verzamelen en opslaan als variable
    value = adc.read_u16() 
    mv = 3300.0 * value / 65535 
    temp = (mv - 500) / 10 
    # Druksensor/weersensordata verzamelen en opslaan als variable
    pressure, humidity =  bmp.raw_values 
    # Data verzenden
    data = f"{temp},{pressure},{humidity},{IDENTIFICATIE}"
    rfm.send(bytes(data, "utf-8"))
    # Shell Logging
    if(SHELL = 1):
        print("Temperatuur: ")
        print(temp)
        print(\n)
        print("Druk: ")
        print(pressure)
        print(\n)
        print("Luchtvochtigheid: ")
        print(humidity)
        print(\n)
    # Slapen
    time.sleep(SLEEP)

