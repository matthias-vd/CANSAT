import board
import busio
import digitalio
import time
import adafruit_rfm69




# Define radio parameters.
RADIO_FREQ_MHZ = 433.3  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\X08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID = 120
BASESTATION_ID = 100

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.GP5)
RESET = digitalio.DigitalInOut(board.GP3)
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT
# Or uncomment and instead use these if using a Feather M0 RFM69 board
# and the appropriate CircuitPython build:
# CS = digitalio.DigitalInOut(board.RFM69_CS)
# RESET = digitalio.DigitalInOut(board.RFM69_RST)


# Initialize SPI bus.
spi = busio.SPI(board.GP6, board.GP7, board.GP4)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
#rfm69.encryption_key = ENCRYPTION_KEY
rfm69.node = NODE_ID

print('freq 	:',rfm69.frequency_mhz)
print('NODE		:',rfm69.node)


# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).


# Print out some chip state:
print("Temperature: {0}C".format(rfm69.temperature))
print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))

# Send a packet.  Note you can only send a packet up to 60 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm69.send(bytes("Hello world!\r\n", "utf-8"))
print("Sent hello world message!")

counter = 1
rfm69.ack_retries = 3 # 3 attempt to receive ACK
rfm69.ack_wait    = 0.5 # 500ms, time to wait for ACK 
rfm69.destination = BASESTATION_ID # Send to specific node 100

print( 'Frequency     :', rfm69.frequency_mhz )
print( 'encryption    :', rfm69.encryption_key )
print( 'NODE_ID       :', NODE_ID )
print( 'BASESTATION_ID:', BASESTATION_ID )
print( '***HEADER***' )
print( ":iteration_count,time_sec,pressure_hpa,tmp36_temp,bmp280_temp;" )
print( '***DATA***' )

while True:  
    print("Send message %i!" % counter)
    ack = rfm69.send(bytes("Message %i!" % counter , "utf-8") )       
    counter += 1
    time.sleep(0.1)


# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.

