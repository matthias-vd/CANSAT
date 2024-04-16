from machine import SPI, Pin
from rfm69 import RFM69
import time

FREQ = 433.1
ENCRYPT = 0

ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 100 # ID of this node

spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4), baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
if ENCRYPT == 1:
    rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID 

print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )

print("Waiting for packets...")
while True:
    packet = rfm.receive(with_ack=True)
    if packet != None:
        print("Received (ASCII):", str(packet, "ascii"))
        print("RSSI (-dBm): ", rfm.last_rssi)
