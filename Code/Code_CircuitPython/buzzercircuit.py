from machine import Pin, PWM
import utime

# Define the pin number for the buzzer
BUZZER_PIN = 14

# Create a PWM object on the buzzer pin
buzzer_pwm = PWM(Pin(BUZZER_PIN))

# Set the initial frequency and duty cycle
frequency = 1000
duty_cycle = 0

# Set the frequency and duty cycle of the PWM signal
buzzer_pwm.freq(frequency)
buzzer_pwm.duty_u16(duty_cycle)

# Set the volume (duty cycle) of the buzzer
def set_volume(volume):
    global duty_cycle
    duty_cycle = int(volume * 65535)
    buzzer_pwm.duty_u16(duty_cycle)

# Set the frequency of the buzzer
def set_frequency(frequency):
    global duty_cycle
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty_u16(duty_cycle)

# Make the buzzer beep for a certain duration (in milliseconds)
def beep(duration):
    buzzer_pwm.duty_u16(duty_cycle // 2)
    utime.sleep_ms(duration)
    buzzer_pwm.duty_u16(duty_cycle)

# Example usage
set_volume(0.1) # Set the volume to 50%
set_frequency(2000) # Set the frequency to 1 kHz
beep(500) # Beep for 500 ms