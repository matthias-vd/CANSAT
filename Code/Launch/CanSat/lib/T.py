from machine import SPI, Pin
from rfm69 import RFM69
import time

 
FREQ           = 433.1

ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"

NODE_ID        = 100 # ID of this node

 

spi = SPI(0, polarity=0, phase=0, firstbit=SPI.MSB) # baudrate=50000,

nss = Pin( 5, Pin.OUT, value=True )

rst = Pin( 3, Pin.OUT, value=False )

 

rfm = RFM69( spi=spi, nss=nss, reset=rst )

rfm.frequency_mhz = FREQ

 

# Optionally set an encryption key (16 byte AES key). MUST match both

# on the transmitter and receiver (or be set to None to disable/the default).

rfm.encryption_key = bytes( [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8] )

rfm.node = NODE_ID # This instance is the node 123

 

print( 'Freq            :', rfm.frequency_mhz )

print( 'NODE            :', rfm.node )

 

print("Waiting for packets...")

while True:

              packet = rfm.receive( with_ack=True )

              # Optionally change the receive timeout from its default of 0.5 seconds:

              # packet = rfm.receive(timeout=5.0)

              # If no packet was received during the timeout then None is returned.

              if packet is None:

                            # Packet has not been received

                            pass

              else:

                            # Received a packet!

                            print( "Received (raw bytes):", packet )

                            # And decode to ASCII text

                            packet_text = str(packet, "ascii")

                            print("Received (ASCII):", packet_text)

                            print("-"*40) 
