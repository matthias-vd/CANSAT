import time 
import busio
import board
import digitalio
from Arducam import * # requires Arducam files to be in same dir as 'code': Arducam.py, ov2640_reg.py (& ov5642_reg.py)
import circuitpython_base64 as b64 # requires package install of: circuitpython-base64
import storage

#Create files to write into
with open('/test.jpg', 'wb'):
   pass
with open('/test.txt', 'wt'):
   pass

# Set up Cam board
mycam = ArducamClass(OV2640)
mycam.Camera_Detection()
mycam.Spi_Test()
mycam.Camera_Init()
time.sleep(1)
mycam.set_format(JPEG)
mycam.OV2640_set_JPEG_size(OV2640_160x120)

def get_still(mycam):
    once_number = 128
    buffer=bytearray(once_number)
    count = 0
    finished = 0
    length = mycam.read_fifo_length()
    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()

    while True:
        
        mycam.spi.readinto(buffer, start=0, end=once_number)
        #print(str(count) + ' of ' + str(length))
        buffer_txt = b64.encodebytes(buffer)
        #print(buffer_txt[:20])
        with open('/test.jpg', 'ab') as fj:
            fj.write(buffer)
        with open('/test.txt', 'at') as ft:
            ft.write(buffer)
        count += once_number
        
        if count + once_number > length:

            count = length - count
            mycam.spi.readinto(buffer, start=0, end=count)
            buffer_txt = b64.encodebytes(buffer)
            print(buffer_txt[:20])
            with open('/test.jpg', 'ab') as fj:
                 fj.write(buffer)
            with open('/test.txt', 'a') as ft:
                 ft.write(buffer_txt)
            mycam.SPI_CS_HIGH()
            mycam.clear_fifo_flag()
            #finished = 1
            return finished
            
        print(buffer)

mycam.flush_fifo()
mycam.clear_fifo_flag()
mycam.start_capture()
finished = 0

teller = 0

while finished == 0:  

    
    if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
        finished = get_still(mycam)
        print(finished)
        time.sleep(1)
        
    teller += 1    
    
print('Finished!')
