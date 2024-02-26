""" CANSAT PICO RECEIVER node

Receives message requiring ACK over RFM69HCW SPI module - RECEIVER node
Must be tested togheter with test_emitter

See Tutorial : https://wiki.mchobby.be/index.php?title=ENG-CANSAT-PICO-RFM69HCW-TEST
See GitHub : https://github.com/mchobby/cansat-belgium-micropython/tree/main/test-rfm69

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071
"""

from machine import SPI, Pin
from rfm69 import RFM69
import time


###############" INITIALIZE RFM ##################

FREQ           = 433.0
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 100 # ID of this node


def dbm_to_mw(dBm):
    """ Transform the power in dBm to its equivalent in milliWatt """
    return 10**((dBm)/10.)

spi = SPI(0, polarity=0, phase=0, firstbit=SPI.MSB) # baudrate=50000,
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )

rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz = FREQ
rfm.bitrate = 250000 # 250 Kbs
rfm.frequency_deviation = 250000 # 250 KHz
rfm.tx_power = 13  # 13 dBm = 20mW (default value, safer for all modules)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node = NODE_ID # This instance is the node 123

print( 'RFM version     :', rfm.version )
print( 'Freq            :', rfm.frequency_mhz )
print( 'Freq. deviation :', rfm.frequency_deviation, 'Hz' )
print( 'bitrate         :', rfm.bitrate, 'bits/sec' )
print( 'tx power        :', rfm.tx_power, 'dBm' )
print( 'tx power        :', dbm_to_mw(rfm.tx_power), 'mW' )
print( 'Temperature     :', rfm.temperature, 'Celsius' )
print( 'Sync on         :', 'yes' if rfm.sync_on else 'no' )
print( 'Sync size       :', rfm.sync_size )
print( 'Sync Word Length:', rfm.sync_size+1, "(Sync size+1)" )
print( 'Sync Word       :', rfm.sync_word )
print( 'CRC on          :', rfm.crc_on )
print( 'Preamble Lenght :', rfm.preamble_length )
print( 'aes on          :', rfm.aes_on )
print( 'Encryption Key  :', rfm.encryption_key )
print( 'Freq            :', rfm.frequency_mhz )
print( 'NODE            :', rfm.node )


########## INITIALIZE DATALOG ##################

file = open('satellite.log', 'a')
file.write("TIJD -- HOOGTE -- TEMP-BMP -- TEMP-TMP -- DRUK \n") ##### PAS AAN NAAR TE VERWACHTEN GEGEVENS 


############# RECEIVE AND SAVE PACKAGES ##############

while True:
    print("Waiting for packets...")
    packet = rfm.receive( with_ack=True )
    t = time.localtime()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        file.write(str(t) + "\t EMPTY PACKET \t " + "\n")
        print("RECEIVED NOTHING")
        # Packet has not been received
        pass
    else:
        # Received a packet!
        print( "Received (raw bytes):", packet)
        # And decode to ASCII text
        packet_text = str(packet, "ascii")
        file.write(str(t) + packet_text + "\n")
        print("Received (ASCII):", packet_text)
        print("-"*40)
    time.sleep(0.5)


