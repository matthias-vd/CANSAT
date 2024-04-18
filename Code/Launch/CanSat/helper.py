import math

#### COUNTERS
"""MEASUREMENT_SPEC = 0
MEASUREMENT_RFM = 0
MEASUREMENT_SD = 0
MEASUREMENT_BMP = 0"""

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
        spec.take_measurements_with_bulb()
        all_values = spec.get_value(1)
        spec.take_measurements()
        all_values_bulb = spec.get_value(1)
        measurements.append(all_values_bulb)
    else:
        print("ERROR: NO SPECTRAL MEASUREMENT")
        
def co2_measurement(sgp,measurements):
    if sgp != None:
        eCO2, TVOC = sgp.iaq_measure()
        print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
        measurements.append([eCO2,TVOC])
    else:
        print("ERROR: NO CO2 MEASUREMENT")

def send_package(rfm,bmp_values,measurements):
    if(rfm != None and bmp_values != None):
        rfm.send(bytes(str(bmp_values),"utf-8"))
        #print(bmp_values)
    else:
        print("ERROR: NO PACKAGE SENT")    
    
def save_measurements_sd(sd,measurements):
    if sd != None:
        with open("/sd/measurements.txt", "a") as file:
            file.write(str(measurements) + '\n')
                #MEASUREMENT_SD = MEASUREMENT_SD + 1
    else:
        print("ERROR: NOT SAVED ON SD")
def save_measurements_local(measurements):
    #pass
    with open("/measurements.txt", "a") as f:
        f.write(str(all_values_bulb) + '\n')
    #print("test")
    
def start_buzzer(h,max_h):
    if  max_h > 500 and h < 100:
                
def print_shell(SHELL,measurements):
        if SHELL == 1:
            print(measurements)
    
