import board
import busio

# Create I2C bus
i2c = busio.I2C(board.GP9, board.GP8)

# Iterate through possible I2C addresses
for address in range(0x07, 0x78):
    try:
        i2c.try_lock()
        if i2c.scan().count(address) > 0:
            print("Found device at address: 0x{:02X}".format(address))
    finally:
        i2c.unlock()