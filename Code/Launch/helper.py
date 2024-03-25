import math

def bmp_measurement(bmp,measurements):
    if bmp != None:
        measurements.append(bmp.temperature)
        measurements.append(bmp.pressure)
        return bmp.temperature,bmp.pressure

def calculate_height(bmp,p0,T0,h0,h,max_h):
    
    ### TODO p0 en T0 bepalen bij opstart satelliet?    
    alpha = -0.0065   # Temperature lapse rate in K/m
    g = 9.80665  # Acceleration due to gravity in m/s^2
    R = 8.314    # Universal gas constant in J/(mol·K)

    h = (bmp.temperature/alpha) * ((bmp.pressure/p0)**(-R*alpha/g)-1) + h0
    
    if h>max_h:
        max_h=h
    
    return h

def spectral_measurement(spec,measurements):
    if spec !=  None:
        spec.take_measurements()
        all_values = spec.get_value(1)
        spec.take_measurements_with_bulb()
        all_values_bulb = spec.get_value(1)
        measurements.append(all_values_bulb)
        print("SPECTRAL MEASUREMENT SUCCEEDED")
    else:
        print("NO SPECTRAL MEASUREMENT")

def send_package(rfm,bmp_values,measurements):
    if(rfm != None and bmp_values != None):
        rfm.send(bytes("kom terug het is al getest u case is klaar","utf-8"))
        #rfm.send(bytes(str(bmp_values),"utf-8"))
        #rfm.send(bytes(str(measurements),"utf-8"))
        #rfm.send(bytes(str(rfm),"utf-8"))
        #print((str(measurements)))
        #print("PACKAGE SENT")
        #ack = rfm69.send(measurements)
    else:
        print("NO PACKAGE SENT")    
    
def save_measurements_sd(sd,measurements):
    try:
        if sd != None:
            with open("/sd/measurements.txt", "a") as file:
                file.write(str(measurements) + '\n')
        else:
            print("NOT SAVED ON SD")
    except OSError:
        print("Connectie SD-kaart verloren mid-flight")
        """try:
            print("SD-kaart proberen herinitialiseren")
            spi_sd = init.init_spi_sd()
            return busio.SPI(GP10, MOSI=GP11, MISO=GP8)
            sd = init.init_sd(spi_sd)
            sd = sdcardio.SDCard(spi_sd, board.GP9)
            vfs = storage.VfsFat(sd)
            storage.mount(vfs, '/sd')
        except:
            print("SD-kaart initialisatie mislukt!")"""

def save_measurements_local(measurements):
    pass
    #with open("/measurements.txt", "a") as f:
    #    f.write(str(all_values_bulb) + '\n')
    #print("test")
    
def start_buzzer(h,max_h):
    if  max_h > 500 and h < 100:
        ### ADD CODE TO START BUZZER
        print("buzzer aan")
        
def print_shell(SHELL,measurements):
        if SHELL == 1:
            print(measurements)
    
